import pandas as pd


class AbricateSample:
    def __init__(self, results):
        self.df = pd.read_csv(
                        results,
                        sep="\t")[["#FILE", "GENE", "%COVERAGE", "%IDENTITY"]]
        self.clean = self.cleanup(self, self.df)

    @staticmethod
    def cleanup(self, df):
        self.df["#FILE"] = self.df["#FILE"].apply(self.cleanname)
        return df

    def cleanname(self, name):
        name = name.split("/")[-1].split(".")[0]
        return name


class AbricateSummary:
    def __init__(self, listofresults):
        self.listofresults = listofresults

    def dataframe(self, covcutoff=60, idcutoff=90):
        listsofdf = []
        for i in self.listofresults:
            i = i[i["%COVERAGE"] > covcutoff]
            i = i[i["%IDENTITY"] > idcutoff]
            listsofdf.append(i)

        df = pd.concat(listsofdf)
        return pd.pivot_table(
                            df,
                            index="#FILE",
                            columns="GENE",
                            values="%IDENTITY",
                            fill_value=0)
