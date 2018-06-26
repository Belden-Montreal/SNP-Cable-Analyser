from sample.end_to_end import EndToEnd
from sample.single_ended import SingleEnded
from multiprocessing.dummy import Pool as ThreadPool
from app.import_dialog import ImportSNPDialog

import xlsxwriter

class Project(object):
    '''
    The project class represents a simple project containing a number of regular samples.
    '''

    def __init__(self):
        self._samples = list()

    def importSamples(self, fileNames, singleEnded):
        pool = ThreadPool()
        self._samples.extend(pool.starmap(self.__createSample, zip(fileNames, [singleEnded]*len(fileNames))))

    def removeSamples(self, names):
        self._samples = [x for x in self._samples if x.getName() not in names]

    def generateExcel(self, outputName, sampleNames, z=False):
        workbook = xlsxwriter.Workbook(outputName+".xlsx", options={'nan_inf_to_errors': True})
        samples = [x for x in self._samples if x.name in sampleNames]
        for i,sample in enumerate(samples):
            try:
                worksheet = workbook.add_worksheet(sample.name)
            except:
                worksheet = workbook.add_worksheet(sample.name+str(i))
            worksheet.write('A1', 'Sample ID:')
            worksheet.write('B1', sample.name)

            cell_format = workbook.add_format({'align': 'center',
                                                'valign': 'vcenter'})
            worksheet.merge_range('A4:A5', "", cell_format)
            worksheet.write('A4', "Frequency")
            for i, f in enumerate(sample.freq):
                worksheet.write(5+i,0, f)

            curPos = 1
            numSignals = sample.portsNumber
            for i, (paramName, parameter) in enumerate(sample.parameters.items()):
                if z is False:
                    param = parameter.getParameter()
                    worksheet.merge_range(3, curPos, 3, curPos+numSignals-1,  "", cell_format)
                    worksheet.write(3,curPos, paramName)
                    keys = sorted(param.keys())
                    for i, key in enumerate(keys):
                        worksheet.write(4,curPos+i, parameter._ports[key])
                        for j,data in enumerate(param[key]):
                            worksheet.write(5+j,curPos+i, data)
            
                    curPos += numSignals
                else:
                    param = parameter.getComplexParameter()
                    worksheet.merge_range(2, curPos, 2, curPos+(numSignals-1)*2,  "", cell_format)
                    worksheet.write(2,curPos, paramName)
                    keys = sorted(param.keys())
                    for i, key in enumerate(keys):
                        worksheet.merge_range(3, curPos+i*2, 3, curPos+i*2+1, "", cell_format)
                        worksheet.write(3,curPos+i*2, parameter._ports[key])
                        worksheet.write(4,curPos+i*2, "real")
                        worksheet.write(4,curPos+i*2+1, "imaginary")
                        for j,data in enumerate(param[key]):
                            worksheet.write(5+j,curPos+i*2, data.real)
                            worksheet.write(5+j, curPos+i*2+1, data.imag)
            
                    curPos += numSignals*2
        workbook.close()

    def findSamplesByName(self, names):
        return [x for x in self._samples if x.getName() in names]

    def numSamples(self):
        return len(self._samples)

    def samples(self):
        return self._samples

    def openImportWindow(self, parent):
        dial = ImportSNPDialog(parent)
        res = dial.getFiles()
        if res:
            self.importSamples(res[1], res[0])

    def __createSample(self, name, singleEnded):
        if singleEnded:
            return SingleEnded(name)
        return EndToEnd(name)
        

