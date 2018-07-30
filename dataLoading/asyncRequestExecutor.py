import ssl
import json
import aiohttp
from dataLoading import authUtils

DEMO_REQUEST_URL= "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/317111/Global/Online/ALL/DT/01-Digi/Wheel-1/Sector2/Station1/OccupancyAllHits_perCh_W-1_St1_Sec2"

executor = None
def getSingletonExecutor():
    global executor
    if executor is None:
        executor = asyncRequestExecutor()
    return executor

class asyncRequestExecutor():
    
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def getMatrixFromProtectedUrl(self, url=DEMO_REQUEST_URL):
        dataJson = await self.getJsonDataFromProtectedUrl(url)
        return self.getMatrix(self.parseJsonResult(dataJson))
    
    async def getJsonDataFromProtectedUrl(self, url=DEMO_REQUEST_URL):
        print("URL: " + url)
        authObj = authUtils.AuthContainer().loadData()
        return await self.getContentFromProtectedUrl(url, authObj)

    async def getContentFromProtectedUrl(self, url, authObj: authUtils.AuthContainer): 
        context = ssl.SSLContext()
        context.load_cert_chain(authObj.pathToCerticate, authObj.pathToCerticatePass, authObj.password)
        result =  await self.session.get(url, ssl=context)
        return await result.content.read()

    def getMatrix(self, valueDictionary):
        hist = valueDictionary.get('hist')
        if isinstance(hist, str):
            raise ValueError("Cannot load data from url")
        return valueDictionary.get('hist').get('bins').get('content')      

    def parseJsonResult(self, jsonString):
        return json.loads(jsonString)