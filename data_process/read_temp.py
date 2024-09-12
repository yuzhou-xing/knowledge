from distutils.log import error
import os
import sys
import re
import json
from check_entity_trans.check_tags_NE_FW_modify_little import check_paire_tags

# import common.dataprocessing as dataprocessing



# 1 en-US refine
def read_refine_enUS(p):
    final_lines = []
    with open(p, encoding='UTF-8') as f:
        content =f.read().strip()
        if not content:
            print(f'{p} is empty!')
            return final_lines
        if '\n' in content:
            print(f'Format Error: {p}')
            content = content.replace('\n', '')
        try:
            prefix, text = content.split('\t', 1)
        except ValueError:
            text = content
       
        text = re.sub(r'(<\d+\.\d+\s?\d+\.\d+>)', lambda x: '\n'+x.group(1), text).strip()
        lines = text.split('\n')
        for line in lines:
            time_value, trans = line.split('>', 1)
            try:
                start, end = time_value.strip('<').split(' ', 1)
            except Exception:
                start = end = time_value.strip('<')
            final_lines.append(f'{start}\t{end}\t\t{trans}')
    return final_lines

# isoftstone he-IL
def read_isoft(p):
# def read(p):
    final_lines = []
    
    try:
        with open(p, encoding='UTF-8-sig') as f:
            lines = f.readlines()
    except Exception:
        encoding = dataprocessing.get_encoding(p)
        with open(p, encoding=encoding) as f:
            print(p, encoding)
            lines = f.readlines()
    finally:
        for line in lines:
            line = line.strip()
            if line:
                try:
                    time_value, values = line.split(']', 1)
                    start, end = time_value.split(' ', 1)
                    start = start.strip('[]')
                    end = end.strip('[]')
                    sid, trans = values.strip().split(' ', 1)
                except Exception:
                    final_lines.append(line)
                else:
                    final_lines.append(f'{start}\t{end}\t{sid}\t{trans}')
    return final_lines

# # magic id-ID ms-MY
def read_magic(p):
# def read(p):
    final_lines = []
    with open(p, encoding='UTF-8-sig') as f:
        for line in f:
            line = line.strip()
            if line:
                time_value, sid, gender, trans  = line.split('\t', 3)
                start, end = time_value.split(',', 1)
                start = float(start.strip('[]'))
                end = float(end.strip('[]'))
                
                final_lines.append(f'{start}\t{end}\t{sid}\t{trans}')
    return final_lines
        
# apptek data
def read_apptek(p):
# def read(p):
    final_lines = []
    with open(p, encoding='UTF-8') as f:
        text = json.load(f)
        segments = text['value']['segments']
        for segment in segments:
            sid = segment['segmentId']
            start = segment['start']
            end = segment['end']
            speakerId = segment.get('speakerId', '')
            content = segment.get('transcriptionData', {}).get('content', '')

            final_lines.append(f'{sid}\t{start}\t{end}\t{speakerId}\t{content}')
    return final_lines

# surfingtech
def read_surfingtech(p, mp):
# def read(p, mp):
    with open(p, encoding='UTF-8') as f:
        text = f.read().strip()
    start = ''
    end = ''
    sid = None
    with open(mp, encoding='UTF-8') as fm:
        for line in fm:
            line = line.strip()
            if line:
                if line.startswith('SRC'):
                    sid = line.split()[-1][:-4]
                elif line.startswith('BEG'):
                    start = float(line.split()[-1])
                elif line.startswith('END'):
                    end = float(line.split()[-1])

    final_lines = [f'{sid}\t{start}\t{end}\t\t{text}']
    return final_lines

# TextGrid
# def read_textgrid(p):
def read(p):
    final_lines = []
    with open(p, encoding='UTF-8') as f:
        start = 0
        end = 0
        sid = 0
        trans = ''
        num = None
        for line in f:
            line = line.strip()
            if line:
                if line.startswith('item [2]'):
                    break
                if line.startswith('intervals ['):
                    start = 0
                    end = 0
                    sid = re.search(r'\[(\d+)]', line).group(1)
                    trans = ''
                    num = re.search(r'\[(\d+)\]', line).group(1)
                elif line.startswith('xmin'):
                    start = float(line.split('=')[-1].strip())
                elif line.startswith('xmax'):
                    end = float(line.split('=')[-1].strip())
                elif line.startswith('text'):
                    trans = line.split('=')[-1].strip().strip('"')
                    if not trans.strip():
                        continue
                    if trans in ['[ ]<Z>', '[ ]<S>']:
                        continue
                    final_lines.append(f'{sid}\t{start}\t{end}\t\t{trans}')
    return final_lines

# add deal with zh_CN
def read_trans_zh_CN(p):
    deal_l = []
    try:
        with open (p,encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(e)
        
    finally:
        for l in lines:
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            try:
                f_p,s_p = s.split(']',1)
                s_time,e_time = f_p.replace('[', '').split(',')
                sid= int(s_p.strip().split()[0])
                len_s = len(s_p.strip().split())
                trans_info = s_p.strip().split()[len_s-1]
            except Exception as e:
                print(e)
            # deal_l.append([s_time,e_time,sid,trans_info])  #f'{sid}\t{start}\t{end}\t\t{trans}'
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
    return deal_l


def read_pacterapublic(p):
    final_lines = []
    temp_list = []
    with open(p, encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    content = json.loads(line)
                    # short audio
                    if len(content['Result']) > 1:
                        start = content['Result'][0]['Body']['Segments'][0]['Start']
                        end = content['Result'][0]['Body']['Segments'][0]['End']
                        segment_id = content['Result'][0]['Body']['Segments'][0]['SegmentID']
                        speaker = content['Result'][1]['Body']['Segments'][0]['Speaker']
                        trans = content['Result'][1]['Body']['Segments'][0]['TranscriptionContent']
                        # segment_id, start, end, sid, trans
                        final_lines.append(f'{segment_id}\t{start}\t{end}\t{trans}')
                    else: #long session
                        segments = content['Result'][0]['Body']['Segments']
                        for seq in segments:
                            start = seq['Start']
                            end = seq['End']
                            sid = seq['SegmentID']
                            if 'TranscriptionContent' in seq.keys():
                                trans = seq['TranscriptionContent']
                            else:
                                trans = seq['transcription']           
                            final_lines.append(f'{sid}\t{start}\t{end}\t\t{trans}')
                except Exception as e:
                    if p not in temp_list:
                        temp_list.append(p)
    print(temp_list[0])
    return final_lines


# read data for 1008
def read_trans_1008(p):
        deal_l = []
        try:
            with open (p,encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            print(e) 
        finally:
            for l in lines:
                s_time = 0
                e_time = 0
                sid = 0
                trans_info = ''
                s = l.strip()
                try:
                    trans_info = s.split("\t")[-1]
                    # temp change
                    time_info,sid,sex,trans_info = s.split('\t',4)
                    time_info = time_info.replace(']', '')
                    s_time,e_time = time_info.replace('[', '').split(',')
                except Exception as e:
                    print(e)
                # deal_l.append([s_time,e_time,sid,trans_info])  #f'{sid}\t{start}\t{end}\t\t{trans}'
                deal_l.append(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
        return deal_l

def read_trans_1011(p):
    deal_l = []
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print("reading tsv file is bad",e) 
    finally:
        for l in lines:
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            single_letter_list = list('/’=&')       #list('１３４５９')  #list('　－１３４５９～')
            single_letter_list.append('szabadságkérelmemet')
            if not s:
                continue
            try:
                f_p,s_p = s.split(']',1)
                s_time,e_time = f_p.replace('[', '').split(' ')
                sid = s_p.strip().split(' ',1)[0]
                if len(s_p.strip().split(' ')) == 1:
                    continue
                trans_info = s_p.strip().split(' ',1)[1]#.replace('[OVERLAP]','<OVERLAP>').replace('[OVERLAP/]','<OVERLAP/>').replace('[OVERLAP ]','<OVERLAP >')
                # print(re.sub('<.*?>',' ',trans_info))
                # sys.exit()
                # if ' ' in trans_info:# or '{' in trans_info or '}'in trans_info:#'Ｖ' in trans_info or 'ｈ' in trans_info or 'ｍ' in trans_info: # if '"' in trans_info or '|' in trans_info or '/' in re.sub('<.*?>',' ',trans_info):
                #    print(p)
                # for single_letter in single_letter_list:
                #     if single_letter in re.sub('<.*?>',' ',trans_info):
                #         print(p,'\t',single_letter)

            except Exception as e:
                print("reading tsv file is bad",e) 
                print(os.path.basename(p),l)
                raise "reading tsv file is bad"
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
            # print(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
    return deal_l
    # return ''

def read_trans_1011_simple(p):
    deal_l = []
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print("reading tsv file is bad",e) 
    finally:
        for order,l in enumerate(lines):
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            if not s:
                continue
            try:
                s_time,e_time = order,order+1
                sid = 'S1'
                # if len(s_p.strip().split(' ')) == 1:
                #     continue
                # filename,trans_info = l.strip().split('\t')

                fileName = l.strip().split('\t')[0]
                trans_info = l.strip().split('\t')[1]
                # trans_info = re.sub('\[\d+(\.\d+)? \d+(\.\d+)?\]',' ', trans_info.replace('<OL>','<OVERLAP>').replace('</OL>','<OVERLAP/>'))

            except Exception as e:
                print("reading tsv file is bad",e) 
                print(os.path.basename(p),l)
                raise "reading tsv file is bad"
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
            # print(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
    return deal_l


def read_trans_fairness(p):
    deal_l = []
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print("reading tsv file is bad",e) 
    finally:
        filename = os.path.splitext(os.path.basename(p))[0]
        for order,l in enumerate(lines):
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()


            if not s:
                continue
            try:
                s_time,e_time = order,order+1
                sid = 'S1'

                if order != 0:
                    filename = filename+'_'+"{:03d}".format(order+1)
                
                trans_info = trans_info+' '+l.strip()
                    # if '\'
                # trans_info = trans_info.replace('<OL>','<OVERLAP>').replace('</OL>','<OVERLAP/>')

            except Exception as e:
                print("reading tsv file is bad",e) 
                print(os.path.basename(p),l)
                raise "reading tsv file is bad"
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
            # print(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
            #
    # single_letter_list = list('$+}¨')
    # for single_letter in single_letter_list:
    #     if single_letter in re.sub('<.*?>','',trans_info):
    #         print(p,'\t',single_letter)
    return deal_l
    # return ""


def read_trans_isoft_dictation(p,flag_format = None):
    deal_l = []
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print("reading tsv file is bad",e) 
    finally:
        for i,l in enumerate(lines):
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            if not s:
                continue
            try:
                f_p,s_p = s.split(']',1)
                s_time,e_time = f_p.replace('[', '').split(' ')
                sid = i
                trans_info = s_p.strip()#.split(' ',1)[1]
            except Exception as e:
                print("reading tsv file is bad",e) 
                print(os.path.basename(p),l)
                raise "reading tsv file is bad"
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
            print(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
    if flag_format.lower() == 'display':
        return deal_l,lines
    return deal_l,None

def read_trans_rockfall(p):
    deal_l = []
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print("reading tsv file is bad",e) 
    finally:
        for l in lines:
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            if not s:
                continue
            try:
                s_time,e_time,sid,trans_info = s.split('\t')
                s_time = int(s_time)/10000000
                e_time = int(e_time)/10000000
                # f_p,s_p = s.split(']',1)
                # s_time,e_time = f_p.replace('[', '').split(' ')
                # sid = s_p.strip().split(' ',1)[0]
                # trans_info = s_p.strip().split(' ',1)[1]
            except Exception as e:
                print("reading tsv file is bad",e) 
                print(os.path.basename(p),l)
                raise "reading tsv file is bad"
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
            # print(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
    return deal_l

#online meeting set|FY23Q4-IS-Flexible-Collection-TX
def read_trans_1011_uk_UA(p):
    deal_l = []
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print("reading tsv file is bad",e) 
    finally:
        flag = False
        for i,l in enumerate(lines):
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            if flag:
                flag = False
                continue
            if not s:
                continue
            try:
                if i+1 < len(lines) and'[' not in lines[i+1] and lines[i+1].strip() != '':
                    f_p,s_p = s.split(']',1)
                    s_time,e_time = f_p.replace('[', '').split(' ')
                    sid = s_p.strip().split(' ',1)[0]
                    trans_info = '{} {}'.format(s_p.strip().split(' ',1)[1],lines[i+1].strip())
                    flag = True
                else:
                    f_p,s_p = s.split(']',1)
                    s_time,e_time = f_p.replace('[', '').split(' ')
                    sid = s_p.strip().split(' ',1)[0]
                    trans_info = s_p.strip().split(' ',1)[1]
            except Exception as e:
                print("reading tsv file is bad",e) 
                print(os.path.basename(p),l)
                raise "reading tsv file is bad"
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
            print(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
            with open(r"D:\v-yuhangxing\data\FY23Q4-IS-Flexible-Collection-TX\Delivery\uk-UA_07152023\test.txt",'a+',encoding='utf8') as test:
                test.write(f'{os.path.basename(p)}\t{sid}\t{s_time}\t{e_time}\t\t{trans_info}\n')
    return deal_l

#it-IT
def read_trans_1011_SpeechDomain_Entity(p):
    deal_l = []
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print("reading tsv file is bad",e) 
    finally:
        for l in lines:
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            if not s:
                continue
            try:
                f_p,s_p = s.split(']',1)
                s_time,e_time = f_p.replace('[', '').split(' ')
                sid = s_p.strip().split(' ',1)[0]
                trans_info = s_p.strip().split(' ',1)[1]
            except Exception as e:
                print("reading tsv file is bad",e) 
                print(os.path.basename(p),l)
                raise "reading tsv file is bad"
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
            print(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
    return deal_l



def read_trans_kundata(p):
    deal_l = []
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print("reading kun trans file is bad",e) 
    finally:
        for l in lines:
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            if not s:
                continue
            try:
                f_p,s_p = s.split(']',1)
                s_time,e_time = f_p.replace('[', '').split(',')
                sid = s_p.strip().split('\t',1)[0]
                trans_info = s_p.strip().split('\t')[-1]
            except Exception as e:
                print("reading tsv file is bad",e) 
                print(os.path.basename(p),l)
                raise "reading tsv file is bad"
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
            print(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
    return deal_l


def read_temp_json_file(json_p):
    final_lines = []
    with open(json_p,"r",encoding="utf-8-sig") as fr:
        data = json.load(fr)
        data_list = data.get("Segments")
        print(data_list)
        for d in data_list:
            sid = d.get("SegmentID")
            start = d.get("Start",0)
            end = d.get("End",0)
            TranscriptionContent = d.get("TranscriptionContent")
            temp_l = f"{sid}\t{start}\t{end}\t{TranscriptionContent}"
            final_lines.append(temp_l)
    print(final_lines)
    return final_lines

def read_temp_json_file_0404(json_p):
    final_lines = []
    with open(json_p,"r",encoding="utf-8-sig") as fr:
        data = json.load(fr)
        Segments = data["Result"][0]["Body"]["Segments"]
        for s in Segments:
            speaker = s["speaker"]
            Start = s["Start"]
            End = s["End"]
            TranscriptionContent = s["TranscriptionContent"]
            temp_l = f"{speaker}\t{Start}\t{End}\t{TranscriptionContent}"
            final_lines.append(temp_l)
    return final_lines

def read_trans_temp(p):
    deal_l = []
    lines = ''
    try:
        with open (p,encoding="UTF-8-sig") as f:
            lines = f.readlines()
            # print(lines)
    except Exception as e:
        print(e) 
    finally:
        for l in lines:
            s_time = 0
            e_time = 0
            sid = 0
            trans_info = ''
            s = l.strip()
            try:
                f_p,s_p = s.split(']',1)
                s_time,e_time = f_p.replace('[', '').split(',')
                trans_info = s_p.replace("\t",'')
            except Exception as e:
                print(e)
            # print(re.findall('\D.', s_time))
            # print(re.findall('\D.', e_time))
            # print(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
            deal_l.append(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
    return deal_l

def read_txt_for_datatang(fp):
    deal_l = []
    try:
        with open (fp,encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(e) 
    finally:
        for l in lines:
            if l:
                s_time = 0
                e_time = 0.1
                sid = 0
                trans_info = l.strip()
                print(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
                deal_l.append(f'{sid}\t{s_time}\t{e_time}\t\t{trans_info}')
    return deal_l

def read_txt_long_for_datatang(fp):
    deal_l = []
    try:
        with open (fp,encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(e) 
    finally:
        for l in lines:
            if l:
                try:
                    s_time,e_time,sid,trans_info = l.split('\t')
                    trans_info = trans_info.strip()
                    print(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
                    deal_l.append(f'{sid}\t{s_time}\t{e_time}\t{trans_info}')
                except:
                    print(fp)
                    raise "error"
    return deal_l


def read_TextGrid(p,itme_num=1):
    trans_list = []
    start = 0
    end = 0
    trans = ''
    num = None
    item_line_patter = "item \[{}\]".format(itme_num)
    item_other_line_patter = "item \[[^{}]\]".format(itme_num)
    with open(p, encoding='UTF-8') as f:
        is_start = False
        for line in f:
            line = line.strip()
            if line:
                if re.match(item_line_patter,line):
                    is_start = True
                if re.search(item_other_line_patter,line):
                    is_start = False
                if is_start:
                    if line.startswith('intervals ['):
                        start = 0
                        end = 0
                        trans = ''
                        num = re.search(r'\[(\d+)\]', line).group(1)
                    elif line.startswith('xmin'):
                        start = float(line.split('=')[-1].strip())
                    elif line.startswith('xmax'):
                        end = float(line.split('=')[-1].strip())
                    elif line.startswith('text'):
                        if start > end:
                            print(f'Timestamp Error: {start} {end} {p}')
                        trans = line.split('=')[-1].strip().strip('"')
                        if '*' in trans:
                            print(p)
                            sys.exit()
                        if not trans.strip():
                            continue
                        if trans in ['[ ]<Z>', '[ ]<S>', '<S>', '<Z>']:
                            continue
                        temp_l = f"{num}\t{start}\t{end}\t{trans}"
                        trans_list.append(temp_l)
    return trans_list

def read_long_json(fp, flag_format = None):
    trans_list = []
    print(fp)
    with open(fp,'r',encoding='utf-8-sig') as fr:
        data = json.load(fr)
    try:
        body = data["Result"][0]["Body"]
        segments = body['Segments']
    except Exception as e:
        print(e)
        raise "long json file is not right format"
    for item in segments:
        speaker = item["speaker"]
        start = item["Start"]
        end = item["End"]
        transcriptionContent = item["TranscriptionContent"]
        # transcriptionContent = item["transcription"]
        # print(f"{speaker}\t{start}\t{end}\t{transcriptionContent}")
        trans_list.append(f"{speaker}\t{start}\t{end}\t{transcriptionContent}")
    # return trans_list
    if flag_format.lower() == 'display':
        return trans_list,segments
    return trans_list,None
def read_trans_entity(entity_path):
    error_line = []
    if entity_path != []:
        for i,file in enumerate(entity_path):
            try:
                with open(file,'r',encoding='utf-8-sig') as f:
                    lines = f.readlines()
            except Exception as e:
                print("reading txt file is bad",e) 
            finally:
                for line in lines:
                    audio_name,trans_info = line.split('\t')
                    res = check_paire_tags(trans_info)
                    if not res:
                        error_line.append(line)
    return error_line

# if __name__ == "__main__":
#     read_trans_kundata(r"E:\v-feiyuzhang\20230616taskdata\zh-CN\MDT-ASR-G029\DATA\TXT\G0004_S0002_0_SPK006.txt")