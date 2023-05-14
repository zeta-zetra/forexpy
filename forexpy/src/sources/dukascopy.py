import requests
import struct 
import lzma 


def main():
    """
    Downloading Dukascopy data
    """

    local_filename = os.path.join(os.path.abspath(''),'save.bi5')
    url = "https://datafeed.dukascopy.com/datafeed/EURUSD/2012/04/02/18h_ticks.bi5"
    # # url = "https://datafeed.dukascopy.com/datafeed/EURUSD/2023/04/01/BID_candles_min_1.bi5"
    # # # res = requests.get("https://datafeed.dukascopy.com/datafeed/eurusd/2021/05/11/23h_ticks.bi5")
    # # # res_body = res.content

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)


    # fmt = '>3i2f'
    # chunk_size = struct.calcsize(fmt)
    # data = []
    # with lzma.open(local_filename) as f:
    #     while True:
    #         chunk = f.read(chunk_size)
    #         if chunk:
    #             data.append(struct.unpack(fmt, chunk))
    #         else:
    #             break
    # df = pd.DataFrame(data)

    # print(df)
if __name__ == "__main__":
    main()