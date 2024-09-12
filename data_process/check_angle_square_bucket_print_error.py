import os,sys,re,json


def remove_repeat(list_msg):
    unique_ele_list = []
    for item in list_msg:
        if item not in unique_ele_list:
            unique_ele_list.append(item)
    return unique_ele_list

def getAlltags(trans_file,outputpath):
    print(trans_file)
    correct_tag = {'angle':[],'square':[]}
    error_tag = {'angle':[],'square':[]}
    time_stamp = {'angle':[],'square':[]}
    count_run_line = 0
    with open(trans_file,'r',encoding="utf-8") as fr:
        merge_trans_list = fr.readlines()
    patterns = ['OVERLAP', 'OL', 'PName', 'NIS','overlap']
    angle_bracket_list = []    # 角括号
    square_bracket_list = []   # 方括号

    #只有半个括号的
    angle_bracket_list_part = ''    # 角括号
    square_bracket_list_part = ''   # 方括号

    for ind_param,trans in enumerate(merge_trans_list):
        # trans_name = trans.split("\t")[0]
        # trans_info = trans.split("\t")[1]


        #trans_name = trans.split("]")[0]
        #trans_info = trans.split("]")[1]
#check_angle_square_bucket.py
        trans_name = trans.strip().split("\t")[0]
        trans_info = trans.strip().split("\t")[-1]
        if trans.startswith('CompareKey') and ind_param == 0:
            continue
        #trans_name,_,trans_info = trans.strip().split("\t")
        #trans_name,trans_info = trans.strip().split("\t")
        count_run_line += 1

        #if '[,]' in trans_info or '[.]' in trans_info or '¿no?]' in trans_info:
        # if "l'avversario" in trans_info:
        #     print(trans_name)
        #     continue
        #     sys.exit()
        
        
        jangle_bracket_unit = re.findall(r"\<(.*?)\>", trans_info)
        angle_bracket_list = angle_bracket_list+jangle_bracket_unit

        square_bracket_unit = re.findall(r"\[(.*?)\]", trans_info)
        square_bracket_list = square_bracket_list + square_bracket_unit

        angle_bracket_list_part += re.sub(r"\<(.*?)\>",' ', trans_info)
        square_bracket_list_part += re.sub(r"\[(.*?)\]", ' ', trans_info)
    

    Angle_brackets = remove_repeat(angle_bracket_list)
    square_brackets = remove_repeat(square_bracket_list)


    square_brackets_info=square_brackets if square_brackets else None
    angle_brackets_info=Angle_brackets if Angle_brackets else None 

    tags_info =  {'square_brackets_info':[f"[{item}]" for item in square_brackets_info] if square_brackets_info else None,
        'angle_brackets_info':[f"<{item}>" for item in angle_brackets_info] if angle_brackets_info else None
        }
    # tags_info =  {
    # 'angle_brackets_info':[f"<{item}>" for item in angle_brackets_info] if angle_brackets_info else None
    # }
    print("all_tags_list",tags_info)
    # 成对标签
    logs = []
    for order_ind,trans in enumerate(merge_trans_list):
        # trans_name = trans.split("\t")[0]
        # trans_info = trans.split("\t")[1]



        #trans_name = trans.split("]")[0]
        #trans_info = trans.split("]")[1]
        trans_name = trans.strip().split("\t")[0]
        trans_info = trans.strip().split("\t")[-1]
        if trans.startswith('CompareKey') and order_ind == 0:
            continue
        # print(trans)
        # sys.exit()
        #trans_name,_,trans_info = trans.strip().split("\t")
        #trans_name,trans_info = trans.strip().split("\t")
        for pattern in patterns:
            if pattern not in trans_info:
                continue
            res1 = re.search(r'[<\[\(]{}/[>\]\)]'.format(pattern), trans_info)
            if res1 is not None:
                # logs.append('!{} illegal tag exists!'.format(res1.group(0)))
                continue
            pp = r'[<\[\(]/?{}[>\]\)]'.format(pattern)
            res2 = re.findall(pp, trans)
            # print('res2', res2)
            flag = True
            if len(res2) % 2 >0:
                flag = False
            else:
                last = None
                for i, o1 in enumerate(res2):
                    if i == 0 and '/' in o1:
                        flag = False
                    if last and last == o1:
                        flag = False
                    last = o1
            if not flag:
                error_trans_p = os.path.join(os.path.dirname(trans_file),'error_trans.txt')
                with open(error_trans_p,'a',encoding='utf-8') as fw:
                    fw.write(f"{trans_name}\t{trans_info}\n")
                logs.append('!<{}> tag is asymmetrical!'.format(pattern))
    tag_check_res=list(set(logs))
    # 未成对标签信息
    print("list of unpaired labels",tag_check_res)
    print("thought {}行".format(count_run_line))

    correct_tag = {'angle':[],'square':[]}
    
    error_tag = {'angle':[],'square':[]}
    time_stamp = {'angle':[],'square':[]}

    if tags_info['square_brackets_info'] != None:
        for sin_tag in tags_info['square_brackets_info']:
            if re.sub('\[\d+(\.\d+)? \d+(\.\d+)?\]',' ',sin_tag).strip() == '':
                time_stamp['square'].append(sin_tag)
            elif sin_tag.count('[') ==1 and sin_tag.count(']') == 1 and ''.join([x for x in list(sin_tag) if x.strip() != '']) != []:
                correct_tag['square'].append(sin_tag)
            else:
                error_tag['square'].append(sin_tag)
                # print(sin_tag)

    if tags_info['angle_brackets_info'] != None:
        for sin_tag in tags_info['angle_brackets_info']:
            if re.sub('<\d+(\.\d+)? \d+(\.\d+)?\>',' ',sin_tag).strip() == '':
                time_stamp['angle'].append(sin_tag)
            elif sin_tag.count('<') ==1 and sin_tag.count('>') == 1 and ''.join([x for x in list(sin_tag) if x.strip() != '']) != []:
                correct_tag['angle'].append(sin_tag)
            else:
                error_tag['angle'].append(sin_tag)
    
    for ind1,pattern in enumerate(angle_bracket_list_part.split(' ')):
        if '<' in pattern or '>' in pattern:
            if ind1 <5:
                error_tag['angle'].append(pattern+'\t'+' '.join(square_bracket_list_part.split(' ')[0:ind1+5]))
            else:
                error_tag['angle'].append(pattern+'\t'+' '.join(square_bracket_list_part.split(' ')[ind1-5:ind1+5]))

    for order,pattern_s in enumerate(square_bracket_list_part.split(' ')):
        # print(pattern)
        if '[' in pattern_s or ']' in pattern_s:
            if order < 5:
                error_tag['square'].append(pattern+' '.join(square_bracket_list_part.split(' ')[0:order+5]))
            else:
                error_tag['square'].append(pattern+' '.join(square_bracket_list_part.split(' ')[order-5:order+5]))
    #         print(pattern_s,' '.join(square_bracket_list_part.split(' ')[order-5:order+5]))
    #         print(trans_name)
    #         print(square_bracket_list_part)
    #         sav_file(outputpath,'square'+'\t'+pattern_s)

    # print('3',time_stamp)
    # print('1',correct_tag)
    # print('2',error_tag)
    sav_file(os.path.join(outputpath,os.path.basename(trans_file)),time_stamp,'time_stamp:')
    sav_file(os.path.join(outputpath,os.path.basename(trans_file)),correct_tag,'correct_tag:')
    sav_file(os.path.join(outputpath,os.path.basename(trans_file)),error_tag,'error_tag:')
    sav_file(os.path.join(outputpath,os.path.basename(trans_file)),{'tag_check_res':tag_check_res},'tag_check_res:')

    # return tag_check_res
    return correct_tag,error_tag,tag_check_res

def sav_file(outputpath,file_dict,des):
    with open(outputpath,'a+',encoding='UTF8') as sav:
        sav.write('\n'+des+'\n')
        for order,(tag_k,tag_v) in enumerate(file_dict.items()):
                sav.write(tag_k+'\n')
                sav.write(str(tag_v)+'\n')

def check_auth(Correct_tag,Error_tag):
    recode_auth_list = []
    single_file_tag= []
    correct_auth_tag  = ["<OL>","</OL>","<disfluency>", "</disfluency>","<PName>", "</PName>", "</NE>", "<NE:name>", "</NE:name>", "<NE>","<UNKNOWN/>","<SN/>","<FILL/>","<CNOISE/>","<ST/>","<BA/>","<FILLlaugh/>","<FL/>","<PII/>","<FL>"]
    for tag_format,tag_list in Correct_tag.items():
        for single_tag_detail in tag_list:
            if single_tag_detail not in correct_auth_tag:
                recode_auth_list.append(single_tag_detail)
            single_file_tag.append(single_tag_detail)
    for tag_format,tag_list in Error_tag.items():
        for single_tag_detail in tag_list:
            if single_tag_detail not in correct_auth_tag:
                recode_auth_list.append(single_tag_detail)
            single_file_tag.append(single_tag_detail)
    return recode_auth_list,single_file_tag


inputpath = sys.argv[1]
outputpath = sys.argv[2]
all_tag = []
error_tag_all = []
for root,der,files in os.walk(inputpath):
    for file in files:
        if file.endswith('tsv'):# and 'lexical' in file:
            C_tag,E_tag,tag_check_res_result = getAlltags(os.path.join(root,file),outputpath)
            # print('c tag:',C_tag,E_tag) #{'angle': [], 'square': []}
            recode_au_tag,single_file_tag_send = check_auth(C_tag,E_tag)
            all_tag.extend(single_file_tag_send)
            error_tag_all.extend(recode_au_tag)
            if recode_au_tag or tag_check_res_result:
                with open(os.path.join(outputpath,'issue_tag_summary.txt'),'a+',encoding='UTF8') as sav_tag:
                    sav_tag.write('{}\t{}\t{}\n'.format(file,recode_au_tag,tag_check_res_result))
                print(recode_au_tag)

print('all tag:',set(all_tag))
print('error tag:',set(error_tag_all))
                # if recode_au_tag.remove('<OVERLAP/>'):
                #     if '<OVERLAP>' in recode_au_tag:
                #         recode_au_tag.remove('<OVERLAP>')
                #         if recode_au_tag:
                #             sys.exit()
                #         sys.exit()
                #     elif recode_au_tag:
                #         sys.exit()