import logging
import re

class MTMessageParser(object):
    ''' Parser to split the any SWIFT MT Message and provide two dictonary, MTMessageBlockDict and  MTMessageBodyDict '''
    
    def __init__(self):
        self.tag3Regex = '{(.*?)}'
        self.MTMessageText = None
        self.MTMessageBlockDict = {}
        self.MTMessageBodyDict = {}
        logging.info('Instantiating MTMessageParser Class')
    
    def validateMTMessageMessage(self, MTMessageTxt = '' ):
        if MTMessageTxt is not None:
            self.MTMessageText = MTMessageTxt
        if MTMessageTxt.count('{') == MTMessageTxt.count('}'):
            logging.info('Swift MT message is properly enclosed with in curly braces')
        else:
            logging.error('Opening and closing braces of Swift MT message does not match')
        
    def parseMTBlock3OR5(self, block3OR5Text):
        block3OR5List = []
        pattern = re.compile(self.tag3Regex)
        blockPatternList = re.findall(pattern, block3OR5Text)
        
        for eachItem in blockPatternList:
            curentDict = {}
            curentDict[eachItem[:eachItem.find(':')]] = eachItem[eachItem.find(':')+1:]
            block3OR5List.append(curentDict)
        return block3OR5List
    
    def parserMTMessage( self, mtMessage = '' ,finalIndex = '}{S:{SAC:}{COP:S}}'):
        for eachblock in range(1,6):
            startOfBlock = eachblock
            for eachblockEnd in range(startOfBlock,6):
                endOfBlock = eachblockEnd + 1
                currIndexOf = "{"+str(eachblock)+":"
                nextIndexOf = "}{"+str(endOfBlock)+":"
                if nextIndexOf == '}{6:':
                    # nextIndexOf = '}{S:{SAC:}{COP:S}}'
                    nextIndexOf = finalIndex
                if mtMessage.count(currIndexOf) == 0:
                    break
                if mtMessage.count(nextIndexOf) == 0:
                    continue
                try:
                    blockValue = mtMessage[mtMessage.index(currIndexOf)+3:mtMessage.rfind(nextIndexOf)]
                    
                    if blockValue.find('{') >= 0 and blockValue.find('}') >=0:
                        blockValue = self.parseMTBlock3OR5(blockValue)
                except ValueError:
                    self.MTMessageBlockDict[eachblock] = None
                    break
                if blockValue:
                    self.MTMessageBlockDict[eachblock] = blockValue
                    break
        
    def getBlockByKey(self, tagKey):
        if self.MTMessageBlockDict == {}:
            logging.info('MT Message is Not Parsed')
            return None
        return self.MTMessageBlockDict[tagKey] if self.MTMessageBlockDict.has_key(tagKey) else None
    
    def processMTMessageBody(self, tagArray = []):
        # body =  self.MTMessageBlockDict.get(4)[:-1].split('\n')
        # x = ''.join(body)
        x = self.MTMessageBlockDict.get(4)[:-1]
        x = x+':'
        for tag in tagArray:
            if x.find(tag) > 0:
                self.MTMessageBodyDict[tag] = x[x.find(tag)+len(tag)+1:x.find(':',x.find(tag)+len(tag)+1)]


if __name__ == __name__:
    print 'Parent or Base MT Message Parser Ready'
    x = MTMessageParser()
    mt202Msg ='{1:F01GOFAskdkanflksaflksfkslafa4812}{2:O20211skfskfhsddfsdljflsdjfXXlskerfkseljfklsdfl5N}{3:{113:xxxx}{108:P440240008191}}{4:\n:20:52452514524541\n:21:47659857u59\n:32A:130814XXX12000000,00\n:52A:NDSIDGH\nlsafjfsd44     \n:58A:OJOJ879LHOS\n:72:\n/BNF/Blab Blab 123, Olayyy\n//SODFHJJSDFSDOIFJ 97534\n/blab/6FOLJAFHSLLSDFJJ\n-}{5:{MAC:00000000}{CHK:SFLFSLDJFLS}}{S:{SAC:}{COP:S}}'
    tagsInMT202Body = ['20','21','13C','32A','52A','52D','53A','53B','53D','54A','54B','54D','56A','56D','57A','57B','57D','58A','58D','72']
    x.validateMTMessageMessage(mt202Msg)
    x.parserMTMessage(mtMessage=mt202Msg)
    print x.MTMessageBlockDict
    x.processMTMessageBody(tagsInMT202Body)
    print x.MTMessageBodyDict
