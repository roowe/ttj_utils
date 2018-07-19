import pymysql
import grequests
import io
import pandas as pd
import warnings

def fundcode_list():
    db = pymysql.connect("localhost", "root", "root", "ims")
    cur = db.cursor()
    cur.execute("SELECT code, `name` FROM fund")
    results = cur.fetchall()
    cur.close()
    db.close()
    return results


def parse(text):
    buf = io.StringIO(text)
    ret = {}
    ks = ("fS_name", "fS_code", "Data_ACWorthTrend", "Data_netWorthTrend")
    for line in buf:
        vs = line.split("=")
        if len(vs) == 2:
            name = vs[0].split(" ")[1].strip()
            if name in ks:
                val = vs[1].strip("; \r\n")
                ret[name]=val
                #print("line", name, val)
    return ret

def unitMoneyVal(obj):
    s = obj["unitMoney"]
    ##print(s)
    ss = s.split("：")
    if ss[0] == "分红":
        ## 分红：每份派现金0.01元
        return obj["unit_net_value"]/(obj["unit_net_value"]+float(s[8:-1]))
    elif ss[0] == "拆分":
        ## 拆分：每份基金份额折算1.027437份
        return float(s[11:-1])


def fetch_datas(fundList):
    print(fundList)

    rs = (grequests.get("http://fund.eastmoney.com/pingzhongdata/%s.js" % fund[0]) for fund in fundList)
    retList = grequests.map(rs)

    all = pd.DataFrame()
    allRate = pd.DataFrame()
    for ret in retList:
        if ret is None:
            print("some err, maybe timeout")
            continue
        if ret.status_code != 200:
            print(ret.url, ret.reason)
        else:
            kvs = parse(ret.text)
            navDF = pd.read_json(kvs["Data_netWorthTrend"], precise_float=True)
            navDF.rename(columns={"x": "timestamp", "y":"unit_net_value",
                                  "equityReturn":"change_pct"}, inplace=True)
            ##print(navDF)
            accNavDF = pd.read_json(kvs["Data_ACWorthTrend"], precise_float=True)
            accNavDF.rename(columns={0: "timestamp", 1:"acc_net_value"}, inplace=True)
            ##print(accNavDF)
            df = pd.merge(navDF, accNavDF, how="outer", on="timestamp")
            df["acc_net_value"].fillna(0, inplace=True)
            df["timestamp"] = df["timestamp"].apply(lambda x: x/1000)
            df["code"] = kvs["fS_code"].strip("\"'")
            umDF = df[df["unitMoney"]!=""].copy()
            if len(umDF) > 0:
                umDF.sort_values(by="timestamp", ascending=False, inplace=True)
                umDF["rate"] = umDF.apply(unitMoneyVal, axis=1)
                umDF["acc_rate"] = umDF["rate"].cumprod()
                umDF = umDF[["timestamp","code","rate","acc_rate"]]
                allRate = allRate.append(umDF)
                #print(umDF)
            ##print(df)
            all = all.append(df)
    ##print(allRate)
    ##print(all)

    conn = pymysql.connect("localhost", "root", "root", "ims")
    cur = conn.cursor()
    cur.executemany("REPLACE INTO fund_history "
                    "(`code`, `timestamp`, change_pct, unit_net_value, acc_net_value) "
                    "VALUES (%(code)s, %(timestamp)s, %(change_pct)s, %(unit_net_value)s, %(acc_net_value)s)",
                    all.to_dict(orient="records"))
    cur.executemany("REPLACE INTO fund_rate "
                    "(`code`, `timestamp`, rate, acc_rate) "
                    "VALUES (%(code)s, %(timestamp)s, %(rate)s, %(acc_rate)s)",
                    allRate.to_dict(orient="records"))
    conn.commit()
    cur.close()
    conn.close()


def main():
    warnings.filterwarnings("ignore")
    ##fundList = (('502010', '证券公司'),)
    ##fundList = (('502010', '证券公司'),('100032', '中证红利'),('162411', '中证500'),)
    fundList = fundcode_list()
    fetch_datas(fundList)

if __name__ == "__main__":
    main()
