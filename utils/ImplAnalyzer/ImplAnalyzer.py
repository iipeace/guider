#!/usr/bin/env python

import os, sys, time, copy
import argparse, json
import CppHeaderParser as CppHeaderParser
from guider import *

class ImplAnalyzer(object):
    skipBinList = []
    typeList = {}
    targetNm = []
    exceptNm = []
    exceptHeaderList = {}
    exceptBinList = {}
    exceptHeaderApis = {}
    typeListOrig = {}
    typeListRep = {}
    targetHeaderList = []
    skipHeaderList = []
    noConstList = [
        'std::shared_ptr',
    ]
    summaryNmDepth = 0

    vectorStr = 'std::vector<'
    pairStr = 'std::pair<'
    allocStr = 'std::allocator<'
    sptrStr = 'std::shared_ptr<'
    funcStr = 'std::function<'



    @staticmethod
    def removeNamespace(arg, exceptList, nm=''):
        if not '::' in arg:
            return arg

        newList = list()
        for item in arg.split():
            if not '::' in item:
                newList.append(item)
                continue

            # split by < #
            newsList = list()
            slist = item.split('<')

            # remove namespace #
            for sitem in slist:
                if not '::' in sitem:
                    newsList.append(sitem)
                    continue

                # check exception list #
                if len(exceptList) > 0:
                    found = False
                    for word in exceptList:
                        if sitem.startswith(word):
                            found = True
                            break
                    if found:
                        newsList.append(sitem)
                        continue

                pos = sitem.rfind('::')
                if pos > 0:
                    sitem = sitem[pos+2:]

                newsList.append(sitem)

            item = '<'.join(newsList)

            newList.append(item)

        return ' '.join(newList)



    @staticmethod
    def checkCont(method, nmFilter, exFilter=[]):
        # remove default/delete methods #
        if 'default' in method and method['default']:
            return False
        elif 'delete' in method and method['delete']:
            return False

        # check exclusion condition #
        for cond in exFilter:
            if 'path' in method and cond in method['path']:
                return False

        # check inclusion condition #
        if len(nmFilter) == 0:
            found = True
        else:
            found = False

        for nm in nmFilter:
            if method['namespace'].startswith(nm):
                found = True
                break

        return found



    @staticmethod
    def getArgs():
        # argument parser #
        parser = argparse.ArgumentParser(description='made by Peace Lee')
        parser.add_argument('--headerpath', required=False, help='path for headers')
        parser.add_argument('--binpath', required=False, help='path for binaries')
        parser.add_argument('--headerapi', required=False, help='API for headers')
        parser.add_argument('--binapi', required=False, help='API for binaries')
        parser.add_argument('--exceptpath', required=False, help='path for exception')
        parser.add_argument('--exceptapi', required=False, help='API for exception')
        parser.add_argument('--out', required=False, help='path for output')
        parser.add_argument('--depth', required=False, help='depth for namespace')
        parser.add_argument('--filter', required=False, help='filter')
        parser.add_argument('--verbose', required=False, help='verbose')
        parser.add_argument('--config', required=False, help='path for config')

        args = parser.parse_args(sys.argv[1:])

        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)

        # headerpath #
        if args.headerpath:
            headerpath = args.headerpath.split(',')
        else:
            headerpath = []

        # binpath #
        if args.binpath:
            binpath = args.binpath.split(',')
        else:
            binpath = []

        # headerapi #
        if args.headerapi:
            headerapi = args.headerapi.split(',')
        else:
            headerapi = []

        # binapi #
        if args.binapi:
            binapi = args.binapi.split(',')
        else:
            binapi = []

        # exceptpath #
        if args.exceptpath:
            exceptpath = args.exceptpath.split(',')
        else:
            exceptpath = []

        # exceptapi #
        if args.exceptapi:
            exceptapi = args.exceptapi.split(',')
        else:
            exceptapi = []

        # out #
        if args.out:
            out = SysMgr.outPath = args.out
        else:
            out = None

        # depth #
        if args.depth:
            if not args.depth.isdigit():
                SysMgr.printErr('wrong depth type')
                sys.exit(0)

            depth = ImplAnalyzer.summaryNmDepth = long(args.depth)
        else:
            depth = 0

        # config #
        if args.config:
            configlist = args.config.split(',')
        else:
            configlist = []

        # filter #
        if args.filter:
            filters = args.filter.split(',')
        else:
            filters = []

        # verbose #
        if args.verbose and \
            args.verbose.lower() == 'true':
            verbose = True
        else:
            verbose = False

        ret = dict({\
            'headerpath': headerpath,
            'binpath': binpath,
            'headerapi': headerapi,
            'binapi': binapi,
            'exceptpath': exceptpath,
            'exceptapi': exceptapi,
            'filters': filters,
            'configlist': configlist,
            'out': out,
            'depth': depth,
            'verbose': verbose,
        })

        return ret



    @staticmethod
    def getNamespace(method):
        if ImplAnalyzer.summaryNmDepth > 0:
            depth = ImplAnalyzer.summaryNmDepth
            nmlist = method.split('::')
            if len(nmlist) < depth:
                nm = method
            else:
                nm = '::'.join(nmlist[:depth])
        else:
            nm = ''

        return nm



    @staticmethod
    def getMethodsFromHeader(
        filename, nmFilter=[], exFilter=[], prt=False, incParam=False,
        incInline=True, exType={}):
        methodList = {}

        # get parsed object #
        try:
            header = CppHeaderParser.CppHeader(filename)
        except SystemExit:
            sys.exit(0)
        except:
            ImplAnalyzer.exceptHeaderList[filename] = True
            SysMgr.printErr('fail to parse %s' % filename, reason=True)
            return None

        '''
        jsonHeader = header.toJSON()
        header.show()
        '''

        # define using alias list #
        alias = header.usingAliases

        # functions outside class #
        for method in header.functions:
            #jsonObj = json.dumps(str(method), indent=1)
            #print(method['debug'])

            if not ImplAnalyzer.checkCont(method, nmFilter, exFilter):
                if 'namespace' in method:
                    nm = method['namespace']
                else:
                    nm = ''
                method['filename'] = filename
                ImplAnalyzer.exceptHeaderApis[nm + method['debug'].strip()] = method
                continue

            if not incInline and \
                method['inline']:
                continue

            param = ''
            if incParam:
                for item in method['parameters']:
                    param += '%s, ' % item['type'].strip()
                if param == '':
                    param = '()'
                else:
                    param = '(%s)' % param[:-2]

            # get namespace #
            if 'namespace' in method:
                nm = method['namespace']
                if nm.endswith('::'):
                    nm = nm.rstrip('::')
            else:
                nm = ''

            infoDict = {
                'filename': filename,
                'namespace': nm,
                'type': '',
                'line': method['line_number'],
                'ret': method['rtnType'],
                'retref': method['returns_reference'],
                'retaddr': method['returns_pointer'],
                'retclass': method['returns_class'],
                'operator': method['operator'],
                'static': method['static'],
                'extern': method['extern'],
                'override': method['override'],
                'inline': method['inline'],
                'template': method['template'],
            }

            methodInfo = "%s%s%s" % (method['namespace'], method['name'], param)
            methodList[methodInfo] = infoDict
            if prt:
                print(methodInfo)

        # methods in in C++ classses #
        for name, val in header.classes.items():
            '''
            val.show()
            print(name, val.get_all_method_names())
            print(name, val.get_all_pure_virtual_methods())
            print(name, val.get_all_methods())
            '''

            for ctype, value in val['methods'].items():
                if ctype in exType:
                    continue

                for method in value:
                    #jsonObj = json.dumps(str(method), indent=1)
                    #print(method['debug'])

                    # get fields #
                    name = method['name']
                    param = ImplAnalyzer.getParams(method, alias)
                    nm = ImplAnalyzer.getNamespace(method['path'])
                    if 'doxygen' in method:
                        doxygen = method['doxygen']
                    else:
                        doxygen = ''

                    # apply for filter #
                    if not ImplAnalyzer.checkCont(method, nmFilter, exFilter):
                        methodInfo = '%s::%s%s' % (method['path'], name, param)
                        method['filename'] = filename
                        ImplAnalyzer.exceptHeaderApis[methodInfo] = method
                        continue

                    # get flags #
                    isConstructor = method['constructor']
                    isDestructor = method['destructor']
                    isConst = method['const']

                    if isDestructor:
                        destructChar = '~'
                    else:
                        destructChar = ''

                    if isConst:
                        constChar = ' const'
                    else:
                        constChar = ''

                    # build full method string #
                    methodInfo = \
                        "%s::%s%s%s%s" % \
                        (method['path'], destructChar, name, param, constChar)

                    infoDict = {
                        'filename': filename,
                        'namespace': nm,
                        'type': ctype,
                        'line': method['line_number'],
                        'ret': method['rtnType'],
                        'retref': method['returns_reference'],
                        'retaddr': method['returns_pointer'],
                        'retclass': method['returns_class'],
                        'operator': method['operator'],
                        'static': method['static'],
                        'extern': method['extern'],
                        'override': method['override'],
                        'inline': method['inline'],
                        'template': method['template'],
                        'alias': alias,
                        'doxygen': doxygen,
                        }

                    methodList[methodInfo] = infoDict

                    if prt:
                        print(methodInfo)

        if prt:
            print(UtilMgr.convDict2Str(methodList))

        return methodList



    @staticmethod
    def convertPair(arg):
        if not arg.startswith(ImplAnalyzer.pairStr):
            return arg

        newList = []
        parg, pairSuffix = arg.split('>', 1)
        argList = parg[len(ImplAnalyzer.pairStr):].strip().split(',')
        for item in argList:
            item = item.strip()
            # convert original type to specific types #
            if arg not in ImplAnalyzer.typeListRep and \
                item in ImplAnalyzer.typeListOrig:
                item = ImplAnalyzer.typeListOrig[item]

            # remove namespace #
            item = ImplAnalyzer.removeNamespace(
                item, ImplAnalyzer.exceptNm)

            # add item to param list #
            newList.append(item)

        res = '%s%s>%s' % \
            (ImplAnalyzer.pairStr, ', '.join(newList), pairSuffix)
        return res



    @staticmethod
    def convertTypes(arg, nm='', method=None):
        origArg = arg
        suffix = ''

        # convert pair #
        if arg.startswith(ImplAnalyzer.pairStr):
            isPair = True
            argList = arg.rsplit('>', 1)
            if len(argList) == 2:
                parg, pairSuffix = argList
            else:
                return 'PAIR'
            arg = parg[len(ImplAnalyzer.pairStr):].strip()
            suffix = pairSuffix + suffix
        else:
            isPair = False

        # convert shared_ptr #
        if arg.startswith(ImplAnalyzer.sptrStr):
            isSptr = True
            argList = arg.rsplit('>', 1)
            if len(argList) == 2:
                sarg, sptrSuffix = argList
            else:
                return 'SHARED'
            arg = sarg[len(ImplAnalyzer.sptrStr):].strip()
            suffix = sptrSuffix + suffix
        else:
            isSptr = False

        # convert vector #
        if arg.startswith(ImplAnalyzer.vectorStr):
            isVector = True
            argList = arg.rsplit('>', 1)
            if len(argList) == 2:
                varg, vectorSuffix = argList
            else:
                return 'VECTOR'

            # process vector type #
            varg = varg[len(ImplAnalyzer.vectorStr):].strip()

            # allocator #
            if varg.startswith(ImplAnalyzer.allocStr):
                aarg = varg[len(ImplAnalyzer.allocStr):].strip()

                # convert pair params #
                aarg = ImplAnalyzer.convertPair(aarg)

                argList = aarg.rsplit('>', 1)
                rtype, trash = argList
            # pair #
            elif varg.startswith(ImplAnalyzer.pairStr):
                rtype = ImplAnalyzer.convertPair(varg)
            # etc #
            else:
                rtype = varg

            # recomposite vector items #
            suffix = vectorSuffix + suffix
            arg = rtype.strip() + suffix
        else:
            isVector = False

        refRet = False
        refCnt = 0
        while 1:
            if arg.endswith('&'):
                refRet = True
                arg = arg[:-1].strip()
                refCnt += 1
            elif refRet:
                break
            else:
                if refCnt == 0:
                    refRet = False
                break

        if arg.endswith('*'):
            refPoint = True
            arg = arg[:-1]
        else:
            refPoint = False

        key = ' const'
        if arg.endswith(key):
            const = True
            arg = arg[:-len(key)]
        else:
            const = False

        # remove namespace #
        arg = ImplAnalyzer.removeNamespace(arg, ImplAnalyzer.exceptNm, nm)

        # convert original type to specific type #
        if arg not in ImplAnalyzer.typeListRep and \
            arg in ImplAnalyzer.typeListOrig:
            arg = ImplAnalyzer.typeListOrig[arg]

        if isSptr:
            arg = '%s%s>' % (ImplAnalyzer.sptrStr, arg)

        if isVector:
            arg = '%s%s>' % (ImplAnalyzer.vectorStr, arg)

        if const:
            arg = 'const %s' % arg

        if refRet:
            for idx in range(0, refCnt):
                arg = '%s &' % arg
        elif refPoint:
            arg = '%s *' % arg

        return arg



    @staticmethod
    def doBinFilter(method):
        removeItems = [
            "[abi:cxx11]",
        ]

        changeItems = [
            ("std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >", "std::string")
        ]

        # remove version #
        method = method.rsplit('@', 1)[0]

        # remove words #
        for keyword in removeItems:
            method = method.replace(keyword, '')

        # change words #
        for keyword in changeItems:
            orig, new = keyword
            method = method.replace(orig, new)

        # split params #
        mlist = method.split('(', 1)
        if len(mlist) == 2:
            name, param = mlist
            nmpos = name.rfind('::')
            if nmpos > 0:
                nm = name[:nmpos]
            else:
                nm = ''

            # operator() #
            if param.startswith(')('):
                name += '(' + param[0]
                param = param[2:]
            # no args #
            elif param.startswith(')'):
                return method
        else:
            return None

        newList = []
        param, suffix = param.rsplit(')', 1)
        origParam = param

        # convert vector #
        prevPos = 0
        cnt = param.count(ImplAnalyzer.vectorStr)
        for idx in range(0, cnt):
            # get start position for a vector #
            pos = \
                param[prevPos:].find(ImplAnalyzer.vectorStr) + \
                len(ImplAnalyzer.vectorStr) + \
                prevPos

            removeSpos = 0
            removeEpos = 0

            # find start position for delete #
            bcnt = 1
            spos = 0
            while 1:
                spos += 1
                epos = pos + spos
                cur = param[epos]
                if cur == '<':
                    bcnt += 1
                elif cur == '>':
                    bcnt -= 1
                elif cur == ',' and \
                    bcnt == 1:
                    removeSpos = epos
                    break

            # find end position for delete #
            bcnt = 1
            spos = removeSpos
            while 1:
                spos += 1
                cur = param[spos]
                if cur == '<':
                    bcnt += 1
                elif cur == '>':
                    bcnt -= 1
                    if bcnt > 1:
                        continue

                    # recomposite items #
                    removeEpos = spos+1
                    param = param[:removeSpos] + param[removeEpos:]
                    break

            # update previous vector position #
            prevPos = pos + 1

        # split args #
        prevArg = ''
        argList = param.split(',')
        for arg in argList:
            arg = arg.strip()
            if prevArg != '':
                arg = '%s, %s' % (prevArg, arg)
                prevArg = ''

            narg = ImplAnalyzer.convertTypes(arg, nm, method)
            if narg == 'VECTOR' or\
                narg == 'PAIR' or\
                narg == 'SHARED':
                prevArg = arg
                continue

            newList.append(narg)

        newParam = '(%s)%s' % (', '.join(newList), suffix)
        newParam = newParam.replace('>>', '> >')

        finalMethod = '%s%s' % (name, newParam)

        return finalMethod



    @staticmethod
    def getMethodsFromBin(filename, nmFilter=[], prt=False):
        methodList = {}

        cmd = "readelf -I %s -J" % filename
        ret = SysMgr.launchGuider(cmd, stderr=True, log=True)

        output = SysMgr.getOutput(ret[1], progress=True)

        jsonDict = UtilMgr.convStr2Dict(output)
        if not jsonDict or \
            len(jsonDict) == 0 or \
            not 'dynsymTable' in jsonDict:
            ImplAnalyzer.exceptBinList[filename] = True
            return methodList

        dlist = jsonDict['dynsymTable']
        for item, val in dlist.items():
            if val['type'] != 'FUNC' or val['ndx'] == 0:
                continue

            if len(nmFilter) == 0:
                found = True
            else:
                found = False

            for nm in nmFilter:
                if item.startswith(nm):
                    found = True
                    break

            if not found:
                continue

            try:
                item = ImplAnalyzer.doBinFilter(item)
                if not item:
                    continue
            except SystemExit:
                sys.exit(0)
            except:
                SysMgr.printWarn(
                    'Fail to analyze %s because %s' % \
                        (item, SysMgr.getErrMsg()))
                continue

            if ImplAnalyzer.summaryNmDepth > 0:
                depth = ImplAnalyzer.summaryNmDepth
                name = item.split('(', 1)[0]
                nmlist = name.split('::')
                if len(nmlist) < depth:
                    summaryNm = name
                else:
                    summaryNm = '::'.join(nmlist[:depth])
            else:
                summaryNm = ''

            methodList[item] = {
                'filename': filename,
                'namespace': summaryNm,
                'size': val['size'],
                'bind': val['bind'],
                'addr': val['value'],
            }

            if prt:
                print(item)

        if prt:
            print(UtilMgr.convDict2Str(methodList))

        return methodList



    @staticmethod
    def filterFileList(flist):
        if len(ImplAnalyzer.targetHeaderList) == 0:
            return flist

        newList = list()
        for item in flist:
            for prefix in ImplAnalyzer.targetHeaderList:
                if os.path.basename(item).startswith(prefix):
                    newList.append(item)
                    break

        return newList



    @staticmethod
    def getHeaderList(args):
        headerlist = args['headerpath']
        hfiles = list()
        if headerlist:
            if type(headerlist) is str:
                headerlist = headerlist.split(',')

            for header in headerlist:
                items = UtilMgr.convPath(header)
                for header in items:
                    if os.path.isdir(header):
                        tmplist = UtilMgr.getFileList(header.strip())
                        tmplist = ImplAnalyzer.filterFileList(tmplist)
                        hfiles += tmplist
                    elif os.path.isfile(header):
                        hfiles.append(header.strip())

        exceptpath = args['exceptpath']
        exceptlist = list()
        for hfile in hfiles:
            hfilename = os.path.basename(hfile)
            for epath in exceptpath:
                items = UtilMgr.convPath(epath)
                for epath in items:
                    if hfile.startswith(epath) or \
                        hfilename == epath:
                        exceptlist.append(hfile)

        return list(set(hfiles) - set(exceptlist))



    @staticmethod
    def getBinList(args):
        binlist = args['binpath']
        bfiles = list()
        if binlist:
            if type(binlist) is str:
                binlist = binlist.split(',')

            for binary in binlist:
                items = UtilMgr.convPath(binary)
                for binary in items:
                    if os.path.isdir(binary):
                        bfiles += UtilMgr.getFileList(binary.strip())
                    elif os.path.isfile(binary):
                        bfiles.append(binary.strip())

        exceptpath = args['exceptpath']
        exceptlist = list()
        for bfile in bfiles:
            bfilename = os.path.basename(bfile)
            for epath in exceptpath:
                items = UtilMgr.convPath(epath)
                for epath in items:
                    if bfile.startswith(epath) or \
                        bfilename == epath:
                        exceptlist.append(bfile)

        return list(set(bfiles) - set(exceptlist))



    @staticmethod
    def initEnvironment():
        SysMgr.initEnvironment()
        SysMgr.encodeEnable = False



    @staticmethod
    def convert2RepType(string):
        for keyword, val in ImplAnalyzer.typeListRep.items():
            if not val in string:
                string = string.replace(keyword, val)
        return string



    @staticmethod
    def applyEnvVars(
        typeList={}, typeListOrig={}, exceptNm=[], targetNm=[], \
        skipBinList=[], targetHeaderList=[], skipHeaderList=[], \
        typeListRep={}, noConstList=[], summaryNmDepth=0):
        ImplAnalyzer.typeList.update(typeList)
        ImplAnalyzer.typeListOrig.update(typeListOrig)
        ImplAnalyzer.typeListRep.update(typeListRep)
        ImplAnalyzer.targetHeaderList += targetHeaderList
        ImplAnalyzer.skipHeaderList += skipHeaderList
        ImplAnalyzer.targetNm += targetNm
        ImplAnalyzer.exceptNm += exceptNm
        ImplAnalyzer.summaryNmDepth = summaryNmDepth
        ImplAnalyzer.skipBinList += skipBinList
        ImplAnalyzer.noConstList += noConstList



    @staticmethod
    def getMethods(args, exType={}):
        hmethods = {}
        bmethods = {}

        # get header files #
        hfiles = ImplAnalyzer.getHeaderList(args)
        if len(hfiles) == 0:
            SysMgr.printErr('no header file')
        for idx, filename in enumerate(hfiles):
            SysMgr.printStat("start parsing '%s'..." % filename)
            ret = ImplAnalyzer.getMethodsFromHeader(
                filename, ImplAnalyzer.targetNm,
                args['exceptapi'] + ImplAnalyzer.skipHeaderList, exType=exType)
            if ret:
                hmethods.update(ret)
        for item in args['headerapi']:
            hmethods[item] = {
                'filename': '??',
                'namespace': '',
                'line': '??',
                'ret': '??',
                'retref': '??',
                'retaddr': '??',
                'retclass': '??',
                'operator': '??',
                'static': '??',
                'extern': '??',
                'override': '??',
                'inline': '??',
                'template': '??',
            }

        # get binary files #
        bfiles = ImplAnalyzer.getBinList(args)
        for idx, filename in enumerate(bfiles):
            SysMgr.printStat('start analyzing %s...' % filename)

            found = False
            for fn in ImplAnalyzer.skipBinList:
                if filename.endswith(fn):
                    found = True
                    break
            if found:
                continue

            ret = ImplAnalyzer.getMethodsFromBin(
                filename, ImplAnalyzer.targetNm)
            if ret:
                bmethods.update(ret)

        for item in args['binapi']:
            bmethods[item] = {
                'filename': '??',
                'namespace': '',
                'size': 1,
                'addr': 0,
                'bind': '??',
            }

        return hfiles, hmethods, bfiles, bmethods



    @staticmethod
    def isConstItem(item):
        # find item in no const list #
        for word in ImplAnalyzer.noConstList:
            if item.startswith(word):
                return False
        return True



    @staticmethod
    def getParams(method, alias=[]):
        param = ''
        for item in method['parameters']:
            item = item['type'].strip()

            # remove const #
            isConst = False
            if item.startswith('const '):
                item = item.split('const ', 1)[1]
                if item.startswith('std::vector') and not item.endswith(' &'):
                    continue

                if ImplAnalyzer.isConstItem(item):
                    isConst = True

            # remove reference for shared_ptr #
            if item.startswith('std::shared_ptr') and \
                item.endswith(' &'):
                item = item.rsplit(' &', 1)[0]

            # convert type #
            item = ImplAnalyzer.convert2RepType(item)

            # remove namespace #
            origItem = item
            item = ImplAnalyzer.removeNamespace(\
                item, ImplAnalyzer.exceptNm)
            namespace = origItem[:len(item)+1]

            # convert aliases by using #
            for key, val in alias.items():
                item = item.replace(key, val)

            # recover const #
            if isConst:
                item = 'const %s' % item

            param += '%s, ' % item
        if param == '':
            param = '()'
        else:
            param = '(%s)' % param[:-2]

        return param



    @staticmethod
    def mergeConfData(configData, args):
        def stripApi(apis):
            newList = []
            for item in apis:
                m = re.match(r'(\[.*\])?\s*(?P<func>.+)\s\[', item)
                if m:
                    newList.append(m.groupdict()['func'])
                else:
                    newList.append(item)

            return newList

        def getData(configData, variable, name):
            if name in configData:
                if variable[name]:
                    variable[name] = variable[name] + configData[name]
                else:
                    variable[name] = configData[name]

            variable[name] = stripApi(variable[name])

            return variable[name]

        if not configData:
            return args

        args['headerpath'] = getData(configData, args, 'headerpath')
        args['binpath'] = getData(configData, args, 'binpath')
        args['exceptpath'] = getData(configData, args, 'exceptpath')

        args['headerapi'] = getData(configData, args, 'headerapi')
        args['binapi'] = getData(configData, args, 'binapi')
        args['exceptapi'] = getData(configData, args, 'exceptapi')

        args['filters'] = getData(configData, args, 'filters')

        if not args['out'] and 'out' in configData:
            args['out'] = configData['out']
        outPath = list(set(args['out']))
        if outPath:
            SysMgr.outPath = outPath[0]

        return args



    @staticmethod
    def getConfData(fileList):
        confData = {}

        if type(fileList) is str:
            configFileList = fileList.split(',')
        elif type(fileList) is list:
            configFileList = fileList
        else:
            SysMgr.printErr("fail to recognize %s" % fileList)
            return None

        for fname in configFileList:
            ret = SysMgr.loadConfig(fname)
            if ret:
                for key, val in ret.items():
                    if key in confData:
                        confData[key] += val
                    else:
                        confData[key] = val

        return confData



    @staticmethod
    def printResults(
        hfiles=[], hmethods={}, bfiles=[], bmethods={}, args={}):

        filters = args['filters']
        verbose = args['verbose']

        # verbose #
        SysMgr.warnEnable = verbose

        # apply filter #
        if filters:
            for key in list(hmethods.keys()):
                for item in filters:
                    if not item in key:
                        hmethods.pop(key, None)

            for key in list(bmethods.keys()):
                for item in filters:
                    if not item in key:
                        bmethods.pop(key, None)

        cv = UtilMgr.convNum

        # Total Header Class #
        imethods = {}
        totalHeaderFunc = {}
        inlineHeaderFunc = {}
        if ImplAnalyzer.summaryNmDepth:
            for method, value in hmethods.items():
                try:
                    # get namespace #
                    nm = value['namespace']

                    # add inline function #
                    if value['inline']:
                        imethods[method] = value
                        inlineHeaderFunc.setdefault(nm, 0)
                        inlineHeaderFunc[nm] += 1

                    totalHeaderFunc.setdefault(nm, 0)
                    totalHeaderFunc[nm] += 1
                except:
                    SysMgr.printErr(SysMgr.getErrMsg())

        # Total Bin Class #
        totalBinFunc = {}
        if ImplAnalyzer.summaryNmDepth:
            for method, value in bmethods.items():
                try:
                    nm = value['namespace']
                    totalBinFunc[nm] += 1
                except:
                    totalBinFunc[nm] = 1

        # remove 0-size methods from binary list #
        zmethods = {}
        for method in list(bmethods.keys()):
            if bmethods[method]['size'] == 0:
                bval = bmethods.pop(method, None)
                zmethods[method] = bval

        # APIs only in Header #
        onlyHList = list(set(hmethods) - set(bmethods) - set(imethods))
        onlyHFunc = {}
        if ImplAnalyzer.summaryNmDepth:
            for item in onlyHList:
                try:
                    nm = hmethods[item]['namespace']
                    onlyHFunc[nm] += 1
                except:
                    onlyHFunc[nm] = 1
        nrOnlyHeader = len(onlyHList)
        nrHMethods = len(hmethods)
        nrIMethods = len(imethods)
        nrCMethods = nrHMethods - nrOnlyHeader

        try:
            perImpHeader = '%.1f' % (nrCMethods / float(nrHMethods) * 100)
        except:
            perImpHeader = '0'

        # APIs only in Binary #
        onlyBList = list(set(bmethods) - set(hmethods))
        onlyBFunc = {}
        if ImplAnalyzer.summaryNmDepth:
            for item in onlyBList:
                try:
                    nm = bmethods[item]['namespace']
                    onlyBFunc[nm] += 1
                except:
                    onlyBFunc[nm] = 1
        nrOnlyBin = len(onlyBList)
        nrBMethods = len(bmethods)
        try:
            perImpBin = '%.1f' % (nrCMethods / float(nrBMethods) * 100)
        except:
            perImpBin = '0'

        # Common APIs #
        commonList = list(set(hmethods) - set(onlyHList) - set(imethods))
        nrCMethods = len(commonList)
        commonFunc = {}
        if ImplAnalyzer.summaryNmDepth:
            for item in commonList:
                try:
                    nm = hmethods[item]['namespace']
                    commonFunc[nm] += 1
                except:
                    commonFunc[nm] = 1

        #-------------------- PRINT --------------------#
        SysMgr.printPipe()

        # Header #
        nrTotalHFile = len(hfiles)
        nrWrongHFile = len(ImplAnalyzer.exceptHeaderList)
        exHList = ImplAnalyzer.exceptHeaderApis
        nrParseHFile = nrTotalHFile - nrWrongHFile
        SysMgr.printPipe((
            '[ Header Summary ] '
            '(TotalAPIs: %s / NormalFiles: %s / AbnormalFiles: %s)') % \
                (cv(nrHMethods), cv(nrParseHFile), cv(nrWrongHFile)))
        SysMgr.printPipe(twoLine)
        SysMgr.printPipe(
            "%25s %s" % ("Impl /  Total (     %)", "Name"))
        SysMgr.printPipe(twoLine)
        val = '%6s / %6s (%5s%%)' % \
            (cv(nrCMethods+nrIMethods), cv(nrHMethods), perImpHeader)
        SysMgr.printPipe('%25s %s' % (val, 'TOTAL'))
        if len(totalHeaderFunc) > 0:
            SysMgr.printPipe(oneLine)

        # Header Summary #
        for method, cnt in sorted(
            totalHeaderFunc.items(), key=lambda e:e[1], reverse=True):
            try:
                impCnt = 0
                if method in commonFunc:
                    impCnt += commonFunc[method]
                if method in inlineHeaderFunc:
                    impCnt += inlineHeaderFunc[method]
                per = '%.1f' % (impCnt / float(cnt) * 100)
            except:
                impCnt = 0
                per = '%.1f' % 0
            val = '%6s / %6s (%5s%%)' % (cv(impCnt), cv(cnt), per)
            SysMgr.printPipe('%25s %s' % (val, method))
        SysMgr.printPipe('%s\n\n\n' % twoLine)

        # Binary #
        nrWrongBFile = len(ImplAnalyzer.exceptBinList)
        nrParseBFile = nrTotalHFile - nrWrongBFile
        SysMgr.printPipe((
            '[ Binary Summary ] '
            '(TotalAPIs: %s / NotImplAPIs: %s / NormalFile: %s / AbnormalFile: %s)') % \
                (cv(nrBMethods), cv(len(zmethods)), cv(nrParseBFile), cv(nrWrongBFile)))
        SysMgr.printPipe(twoLine)
        SysMgr.printPipe(
            "%25s %s" % ("Def /  Total (     %)", "Name"))
        SysMgr.printPipe(twoLine)
        val = '%6s / %6s (%5s%%)' % \
            (cv(len(commonList)), cv(nrBMethods), perImpBin)
        SysMgr.printPipe('%25s %s' % (val, 'TOTAL'))
        if len(totalBinFunc) > 0:
            SysMgr.printPipe(oneLine)

        # Bin Summary #
        for method, cnt in sorted(
            totalBinFunc.items(), key=lambda e:e[1], reverse=True):
            try:
                impCnt = commonFunc[method]
                per = '%.1f' % (impCnt / float(cnt) * 100)
            except:
                impCnt = 0
                per = '%.1f' % 0
            val = '%6s / %6s (%5s%%)' % (cv(impCnt), cv(cnt), per)
            SysMgr.printPipe('%25s %s' % (val, method))
        SysMgr.printPipe('%s\n\n\n' % twoLine)

        # APIs #
        cnt = 0
        SysMgr.printPipe((
            '[ API List ] ([H]eaderOnly: %s / [I]nline: %s / '
            '[B]inOnly: %s / [Z]eroSize: %s / [C]ommon: %s / '
            '[E]xclude: %s)') % \
                (cv(nrOnlyHeader), cv(nrIMethods), cv(nrOnlyBin), \
                cv(len(zmethods)), cv(len(commonList)), cv(len(exHList))))
        SysMgr.printPipe(twoLine)

        # Header APIs #
        for method in sorted(onlyHList):
            mlist = hmethods[method]
            SysMgr.printPipe(
                '[H] %s [ Type: %s / Line: %s / File: %s ]' % \
                (method, mlist['type'], cv(mlist['line']), cv(mlist['filename'])))
        if len(onlyHList) > 0:
            cnt += 1
            SysMgr.printPipe(oneLine)

        # Inline APIs #
        for method, mlist in sorted(imethods.items()):
            SysMgr.printPipe(
                '[I] %s [ Type: %s / Line: %s / File: %s ]' % \
                (method, mlist['type'], cv(mlist['line']), cv(mlist['filename'])))
        if len(imethods) > 0:
            cnt += 1
            SysMgr.printPipe(oneLine)

        # Bin zero-size APIs #
        for method, mlist in sorted(zmethods.items()):
            SysMgr.printPipe(
                '[Z] %s [ Size: %s / Bind: %s / Addr: %s ]' % \
                    (method, cv(mlist['size']), mlist['bind'], hex(mlist['addr'])))
        if len(zmethods) > 0:
            cnt += 1
            SysMgr.printPipe(oneLine)

        # Bin APIs #
        for method in sorted(onlyBList):
            mlist = bmethods[method]
            SysMgr.printPipe(
                '[B] %s [ Size: %s / Bind: %s / Addr: %s ]' % \
                    (method, cv(mlist['size']), \
                    mlist['bind'], hex(mlist['addr'])))
        if len(onlyBList) > 0:
            cnt += 1
            SysMgr.printPipe(oneLine)

        # Common APIs #
        for method in sorted(commonList):
            mlist = bmethods[method]
            hdlist = hmethods[method]
            SysMgr.printPipe(
                '[C] %s [ Type: %s / Size: %s / Line: %s / Bind: %s / Addr: %s ]' % \
                    (method, hdlist['type'], cv(mlist['size']), cv(hdlist['line']), \
                    mlist['bind'], hex(mlist['addr'])))
        if len(commonList) > 0:
            cnt += 1
            SysMgr.printPipe(oneLine)

        # Excluded APIs #
        for method, mlist in sorted(exHList.items()):
            SysMgr.printPipe(
                '[E] %s [ Line: %s / File: %s ]' % \
                    (method, cv(mlist['line_number']), cv(mlist['filename'])))
        if len(exHList) > 0:
            cnt += 1
            SysMgr.printPipe('%s\n\n\n' % oneLine)

        if cnt == 0:
            SysMgr.printPipe('None\n%s' % twoLine)

        SysMgr.printPipe('\n\n')

        # Files #
        SysMgr.printPipe(
            '[ File List ] ([H]eader: %s / [B]in: %s / [E]xcept)' % \
                (cv(nrParseHFile), cv(nrParseBFile)))
        SysMgr.printPipe(twoLine)

        totalCnt = 0

        # Header Files #
        cnt = 0
        for hfile in sorted(ImplAnalyzer.exceptHeaderList.keys()):
            SysMgr.printPipe('[E] %s' % hfile)
            cnt += 1
            totalCnt += 1
        for hfile in sorted(hfiles):
            if hfile in ImplAnalyzer.exceptHeaderList:
                continue
            SysMgr.printPipe('[H] %s' % hfile)
            cnt += 1
            totalCnt += 1
        if cnt > 0:
            SysMgr.printPipe(oneLine)

        # Bin Files #
        cnt = 0
        for bfile in sorted(ImplAnalyzer.exceptBinList.keys()):
            SysMgr.printPipe('[E] %s' % bfile)
            cnt += 1
            totalCnt += 1
        for bfile in sorted(bfiles):
            if bfile in ImplAnalyzer.exceptBinList:
                continue
            SysMgr.printPipe('[B] %s' % bfile)
            cnt += 1
            totalCnt += 1
        if cnt > 0:
            SysMgr.printPipe('%s\n\n\n' % twoLine)

        if totalCnt == 0:
            SysMgr.printPipe('None\n%s' % twoLine)



if __name__ == '__main__':
    # initialize Guider #
    ImplAnalyzer.initEnvironment()

    # load args #
    args = ImplAnalyzer.getArgs()

    # load configuration #
    if args['configlist']:
        config = ImplAnalyzer.getConfData(args['configlist'])
        args = ImplAnalyzer.mergeConfData(config, args)

    # get methods #
    hfiles, hmethods, bfiles, bmethods = \
        ImplAnalyzer.getMethods(args)

    # print methods #
    ImplAnalyzer.printResults(hfiles, hmethods, bfiles, bmethods, args)

    sys.exit(0)

