import os,sys
import copy
import re
# def error_message():


def read_vtt_info(vtt_path, flag_read_QA):
    single_vtt_info = {}
    flag_pattern = [False, False]
    flag_turn_part = False
    qa_info, qa_count = {},0
    turn_final = []
    question_info = {}
    # qa_pattern = [False, False, {}]
    # qa_pattern = [question_type, question,answer_list]
    # qa_pattern = [False, False, False, {}]  #question_type, question, answer_flag, answer_list
    qa_pattern = [False, False,False,{}]
    simple_pair = {}
    # flag_q = False
    single_question_info = {}
    print(vtt_path)
    with open(vtt_path, 'r', encoding='UTF8') as f:
        for i,line in enumerate(f):
            if '------------------------------' in line:
                flag_turn_part = True

            if not flag_turn_part:
                if i == 0:
                    if line.strip() == "WEBVTT":
                        continue
                    else:
                        print('第{}行格式错误'.format(i+1), vtt_path)
                        print('content:',line)
                        sys.exit()

                elif i == 1:
                    if line.strip() == ">":
                        continue
                    else:
                        print('第{}行格式错误'.format(i+1), vtt_path)
                        print('content:',line)
                        sys.exit()
                
                elif not line.strip():
                    continue

                elif '-->' in line.strip():
                    if not flag_pattern[0]:
                        flag_pattern[0] = line.strip()
                
                elif "</v>" in line.strip():
                    if flag_pattern[0] and not flag_pattern[1]:
                        flag_pattern[1] = line.strip()
                    turn_final.append(line.split('\t')[0].split(' ')[-1].replace('>',''))
                    if re.findall('\d',line.split('\t')[0].split(' ')[-1].replace('>','')):
                        pass
                    else:
                        print('turn final error',i,line.split('\t')[0].split(' ')[-1].replace('>',''))
                        sys.exit()
                
                if flag_pattern[0] and flag_pattern[1]:
                    if flag_pattern[0] not in single_vtt_info:
                        single_vtt_info[flag_pattern[0]] = flag_pattern[1]
                        flag_pattern[0], flag_pattern[1] = False, False
                    else:
                        print('same time stamp in one file', flag_pattern[0],vtt_path)

            else:
                if '------------------------------' in line:
                    qa_count += 1
                    continue

                if not line.strip():
                    continue

                if qa_count == 1:
                    if line.strip() != 'Annotated Main Topics':
                        print('topic issue:', vtt_path, line.strip())
                        sys.exit()
                elif qa_count == 2:
                    if "Annotated Main Topics" not in qa_info:
                        qa_info["Annotated Main Topics"] = []
                    qa_info["Annotated Main Topics"].append(line.strip())
                    
                elif qa_count == 3:
                    if line.strip() != 'Queries and Annotated Summaries':
                        print('QA issue:', vtt_path, line.strip())
                        sys.exit()
                else:
                    if line.strip() == 'General Query:' or line.strip() == "Gneral Query:":
                        question_info['General Query'] = {}
                        qa_pattern[0] = 'General Query'
                    elif line.strip() == 'Specific Query:':
                        if qa_pattern[1] and qa_pattern[2]:
                            if len(qa_pattern[2]) == 1:
                                for k,v in qa_pattern[2].items():
                                    if k not in qa_pattern[3]:
                                        qa_pattern[3][k] = v

                                        if qa_pattern[1] not in question_info[qa_pattern[0]]:
                                            question_info[qa_pattern[0]][qa_pattern[1]] = qa_pattern[3]
                                            qa_pattern[1] = False
                                            qa_pattern[2] = False
                                            qa_pattern[3] = {}   
                                        else:
                                            print('line96 error')
                                            sys.exit()          
                                    else:
                                        print('error111')
                                        sys.exit()
                            else:
                                print('error11111')
                                sys.exit()
                        else:
                            print('error11111')
                            sys.exit()
                        question_info['Specific Query'] = {}
                        qa_pattern[0] = 'Specific Query'
                    elif line.strip() == 'Simple Query:' or line.strip() == 'Simple Question:' or line.strip() == 'Simple Quuestion:' or line.strip() == 'Simple Questions:' or line.strip() == 'Simple Query :':
                        if qa_pattern[1] and qa_pattern[2]:
                            if len(qa_pattern[2]) == 1:
                                for k,v in qa_pattern[2].items():
                                    if k not in qa_pattern[3]:
                                        qa_pattern[3][k] = v

                                        if qa_pattern[1] not in question_info[qa_pattern[0]]:
                                            question_info[qa_pattern[0]][qa_pattern[1]] = qa_pattern[3]
                                            qa_pattern[1] = False
                                            qa_pattern[2] = False
                                            qa_pattern[3] = {}   
                                        else:
                                            print('line96 error')
                                            sys.exit()          
                                    else:
                                        print('error111')
                                        sys.exit()
                            else:
                                print('error11111')
                                sys.exit()
                        else:
                            print('error11111')
                            sys.exit()

                        question_info['Simple Query'] = {}
                        qa_pattern[0] = 'Simple Query'

                    else:
                        if line.strip().lower().startswith('query') or line.strip().lower().startswith('question'):
                            if not qa_pattern[1]:
                                qa_pattern[1] = line.strip()
                                # qa_pattern[1] = line.strip().split(':')[0].split(' ',1)[-1]
                            elif qa_pattern[2]:
                                # qa_pattern[1] = line.strip()
                                # print(vtt_path, i)
                                if len(qa_pattern[2]) == 1:
                                    for k,v in qa_pattern[2].items():
                                        if k not in qa_pattern[3]:
                                            qa_pattern[3][k] = v
                                            qa_pattern[2] = False
                                        else:
                                            print('error111')
                                            sys.exit()

                                    if qa_pattern[1] not in question_info[qa_pattern[0]]:
                                        question_info[qa_pattern[0]][qa_pattern[1]] = qa_pattern[3]
                                        qa_pattern[1] = line.strip()
                                        qa_pattern[3] = {}

                                    else:
                                        print(vtt_path+ '包含的问题重复：'+ qa_pattern[0]+"\t"+qa_pattern[1]) 
                                        sys.exit()
                                else:
                                    print('logic error')
        
                            else:
                                print('error in answer flag',vtt_path)
                                sys.exit()

                        elif (line.strip().lower().startswith('relevant') and ':' in line) or (line.strip().lower().startswith('relevent') and ':' in line) :
                            if qa_pattern[2] and len(qa_pattern[2]) == 1:
                                for k,v in qa_pattern[2].items():
                                    if k not in qa_pattern[3]:
                                        qa_pattern[3][k] = v
                                        qa_pattern[2] = {line.strip().split(':')[0].strip()+':': [line.strip().split(':')[1].strip()]}
                                    else:
                                        print('error222')
                                        sys.exit()

                            # if not qa_pattern[2] and 'Relevent Text Spans' not in qa_pattern[3]:
                            #     qa_pattern[3]['Relevent Text Spans'] = line.strip()
                            # else:
                            #     print('error in span')
                            #     sys.exit()

                        elif line.strip().lower().startswith('answe'):
                            if line.strip().split(':')[1].strip() != '':
                                if qa_pattern[2]:
                                    # print('qa_pattern[2] key error',vtt_path)
                                    # sys.exit()
                                    if len(qa_pattern[2].keys()) == 1:
                                        for k,v in qa_pattern[2].items():
                                            qa_pattern[3][k] = v
                                            # qa_pattern[2] = False
                                            qa_pattern[2] = {line.strip().split(':')[0].strip()+':': [line.strip().split(':')[1].strip()]}
                                    else:
                                        print('length error')
                                        sys.exit()

                                # elif line.strip().split(':')[0].strip() not in qa_pattern[3]:
                                #     qa_pattern[3][line.strip().split(':')[0].strip()] = line.strip().split(':')[1].strip()
                                    # qa_pattern[2] = False
                                else:
                                    qa_pattern[2] = {line.strip().split(':')[0].strip()+':': [line.strip().split(':')[1].strip()]}
                            else:
                                if qa_pattern[2]:
                                    if len(qa_pattern[2]) == 1:
                                        for k,v in qa_pattern[2].items():
                                            qa_pattern[3][k] = v
                                            # qa_pattern[2] = False
                                            qa_pattern[2] = {line.strip(): []}
                                    else:
                                        print('error123')
                                        sys.exit()
                                else:
                                    qa_pattern[2] = {line.strip(): []}
                                    # qa[2].append(line.strip())
                                # elif qa_pattern[1]:
                                #     # if line.strip() not in 
                                #     qa_pattern[2] = {line.strip():{}}
                                # else:
                                #     print('error1')
                                #     sys.exit()
                            
                        elif qa_pattern[1] and qa_pattern[2]:
                            temp_final_val = [x for x in qa_pattern[2]][-1]
                            qa_pattern[2][temp_final_val].append(line.strip())

                            # if (qa_pattern[2][0] not in qa_pattern[3]) and (len(qa_pattern[2]) == 1):
                            #     qa_pattern[3][qa_pattern[2][0]] = line.strip()
                            #     qa_pattern[2] = False
                        else:
                            print('error2')
                            sys.exit()



                    # if flag_q != question_info[list(question_info.keys())[-1]]:
                    #     question_info[flag_q] = {qa_pattern[0]:qa_pattern[2]}
                    #     qa_pattern = [False, False, {}]

    if flag_read_QA:
        if qa_pattern[3] and (qa_pattern[1] not in question_info[qa_pattern[0]]):
            question_info[qa_pattern[0]][qa_pattern[1]] = qa_pattern[3]
        else:
            print('line156 error')
            sys.exit()

    if "Queries and Annotated Summaries" not in qa_info:
        qa_info["Queries and Annotated Summaries"] = question_info

    if sorted(turn_final, key=int) != turn_final:
        print('turn的顺序有误',vtt_path)
        # print(sorted(turn_final, key=int))
        # print(turn_final)
        sys.exit()
    qa_info['all_turn'] = [int(x) for x in turn_final]

    if flag_read_QA:
        return single_vtt_info, qa_info
    else:
        return single_vtt_info




# input = r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\Meeting_QA_task\240814\data"
output = r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\Meeting_QA_task\240814\output1"
# input = r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\Meeting_QA_task\240814\data_test"
input = r"E:\v-yuhangxing\data\FY24Q2-IS-Flexible-Data-Collection-TX\Meeting_QA_task\240814\data_refine"
# output = r"E:\Git_env_manage\solve_conflusion\test\work\out"

vtt_info = {}
for root1,der1,files1 in os.walk(input):
    for catalog_type in der1:
        for root,der, files in os.walk(os.path.join(root1,catalog_type)):
            for file in files:
                if file.endswith('vtt'):
                    if catalog_type not in vtt_info:
                        vtt_info[catalog_type] = {}
                    if file not in vtt_info[catalog_type]:
                        vtt_info[catalog_type][file] = os.path.join(root,file)    
    break


if (set(vtt_info["Annotated data"]) - set(vtt_info["Raw data to be annotated"])) and  (set(vtt_info["Raw data to be annotated"]) - set(vtt_info["Annotated data"])):
    print('vtt: annotated file and raw file not match')
    print('annotated file only:',list(set(vtt_info["Annotated data"]) - set(vtt_info["Raw data to be annotated"])))
    print('raw file only:',list(set(vtt_info["Raw data to be annotated"]) - set(vtt_info["Annotated data"])))

annotated_data_info = {}
annotated_qa_info = {}
raw_data_info = {}
file_other_format = []
for name, vtt_path in vtt_info['Annotated data'].items():
    # try:
    #     annotated_data_info[name],annotated_qa_info[name] = read_vtt_info(vtt_path, True)
    # except Exception as e:
    #     print(e)
    #     file_other_format.append(name)

    annotated_data_info[name],annotated_qa_info[name] = read_vtt_info(vtt_path, True)
    raw_data_info[name] = read_vtt_info(vtt_info["Raw data to be annotated"][name],False)

if file_other_format:
    print('file other format:',file_other_format)
    sys.exit()
#annotated_data_info -->   {filename:{timestamp:trans}}
#annotated_qa_info -->  {filename :{'Annotated Main Topics': [xx,xx], 
#                       'Queries and Annotated Summaries':{
                                # General Query: {Q: {a1:xx, a2:xx}, Q: {a1:xx, a2:xx}},
                                # Specific Query: {Q: {a1:xx, a2:xx, "Relevent Text Spans":xx }, Q: {a1:xx, a2:xx， "Relevent Text Spans":xx}},
                                # Simple Query: {Q: {a1:xx, a2:xx}, Q: {a1:xx, a2:xx}}},
                        #'all_turn': turn_final
# }}

# print(annotated_data_info)
# print(raw_data_info)
print(len(annotated_data_info),len(raw_data_info))
copy_annotated_data = copy.deepcopy(annotated_data_info)
for order_s, (name, single_pair) in enumerate(annotated_data_info.items()):
    for timeStamp,single_trans_c in single_pair.items():
        if single_trans_c.strip() == raw_data_info[name][timeStamp].strip():
            copy_annotated_data[name].pop(timeStamp)
            raw_data_info[name].pop(timeStamp)
        # else:
        #     with open(os.path.join(output,'ori_utts_differ.txt'),'a+', encodings="UTF8") as sav_ori:
        #         sav_ori.write('{}\t{}\t{}\n'.format(name, raw_data_info[name][timeStamp].strip(),single_trans_c.strip(),))

    if not copy_annotated_data[name]:
        copy_annotated_data.pop(name)
    if not raw_data_info[name]:
        raw_data_info.pop(name)
# if set(raw_data_info) - set(copy_annotated_data):
#     for
#     with open(os.path.join(output, 'ori_utts_differ.txt'), 'a+', encodings="UTF8") as sav_ori:
#         sav_ori.write('{}\t{}\t{}\n'.format(name, raw_data_info[name][timeStamp].strip(), single_trans_c.strip(), ))

print('annotated and raw 原始内容不对应的部分见：')
print('-'*20)
print('remain annotated data:',copy_annotated_data)
print('remain raw data:',raw_data_info)
print('-'*20)



#annotated_qa_info -->  {filename :{'Annotated Main Topics': [xx,xx], 'Queries and Annotated Summaries':{
        # General Query: {Q: {a1:xx, a2:xx}, Q: {a1:xx, a2:xx}},
        # Specific Query: {Q: {a1:xx, a2:xx, "Relevent Text Spans":xx }, Q: {a1:xx, a2:xx， "Relevent Text Spans":xx}},
        # Simple Query: {Q: {a1:xx, a2:xx}, Q: {a1:xx, a2:xx}},
        # 'all_turn': turn_final
copy_annotated_qa = copy.deepcopy(annotated_qa_info)

title_duplicated = []
qas_type_select = []
name_select = []
for order_qa,(name, qa_part) in enumerate(annotated_qa_info.items()):
    temp_turn_all = []
    title_duplicated_num = []

    if len(qa_part['Annotated Main Topics']) > 1:
        with open(os.path.join(output, 'title_duplicated.txt'), 'a+',encoding='UTF8') as sa_topic:
            sa_topic.write('多个topic：{}\n'.format(name))
    for order_topic, main_topic in enumerate(qa_part['Annotated Main Topics']):
        # print(main_topic,name)
        # print(main_topic.lower().strip().split(')')[0].split('(')[-1].replace('turn','').split('-'))
        temp_turn = main_topic.lower().strip()

        if temp_turn.count('(') == temp_turn.count(')'):
            if '-' in main_topic.lower():
                temp_turn = re.findall('\(\s*.*?\s*(\d+)\s*-\s*(\d+)\s*\)',temp_turn)
            elif '–' in main_topic.lower():
                temp_turn = re.findall('\(\s*.*?\s*(\d+)\s*–\s*(\d+)\s*\)',temp_turn)
                print('[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]',name)
            else:
                print('other char in main topic',name,main_topic) 
                sys.exit()
            # print('-------',temp_turn,name)

            if len(temp_turn) > 1:
                with open(os.path.join(output, 'title_duplicated.txt'), 'a+',encoding='UTF8') as sa_topic:
                    sa_topic.write('单条数据多个标注：{}\t{}\n'.format(name, main_topic))

            for pair_turn in temp_turn:
                # print(pair_turn)
            # temp_turn = list(range(int(temp_turn[0].strip()),int(temp_turn[1].strip())+1))
                pair_turn = list(range(int(pair_turn[0]),int(pair_turn[1])+1))
                for single_pair_turn in pair_turn:
                    if single_pair_turn not in temp_turn_all:
                        temp_turn_all.append(single_pair_turn)
                    else:
                        title_duplicated_num.append(single_pair_turn)
                    
        else:
            print('main topic的左右括号不成对',name,temp_turn.count('('),temp_turn.count(')'))
            sys.exit()
    if title_duplicated_num:
        # title_duplicated.append('{}\t{}'.format(name, title_duplicated_num))
        with open(os.path.join(output, 'title_duplicated.txt'), 'a+',encoding='UTF8') as sa_topic:
            sa_topic.write('{}\t{}\n'.format(name,title_duplicated_num))


    sav_remain = list(set(copy_annotated_qa[name]['all_turn']) - set(temp_turn_all))
    sav_remain1 = list(set(temp_turn_all) - set(copy_annotated_qa[name]['all_turn']))
    # print(sav_remain,sav_remain1)
    #name, 统计转场独有数目，topic独有数目，统计转场-topic， topic- 统计转场
    with open(os.path.join(output, 'turn_del.txt'), 'a+',encoding='UTF8') as sa_turn:
        sa_turn.write('{}\t{}\t{}\t{}\t{}\n'.format(name,len(sav_remain),len(sav_remain1),sav_remain,sav_remain1))

    answer_recode_error = []
    # specific_query_relevent_flag = False
    part_sav_info = {'revelant_span': [], 'sav_pattern': []}

    single_file_q_info,single_file_a_info = [],[]
    for order_qas,(qas_type, qas_detail) in enumerate(qa_part['Queries and Annotated Summaries'].items()):
        qas_type_select.append(qas_type)


        for q_detail, a_detail_dict in qas_detail.items():
            if q_detail.split(':',1)[1].strip() not in single_file_q_info:
                single_file_q_info.append(q_detail.split(':',1)[1].strip())
            else:
                with open(os.path.join(output, 'qa_format.txt'), 'a+',encoding='UTF8') as sa_turn_01:
                    sa_turn_01.write('q\t{}\t{}\n'.format(name, q_detail.split(':',1)[1].strip()))

            #         sa_topic1.write('{}\n'.format(name)) 

            for a_key, a_value in a_detail_dict.items():    #a_value -- list()
                temp_v_a = ' '.join(a_value).strip()
                if temp_v_a not in single_file_a_info:
                    single_file_a_info.append(temp_v_a)
                else:
                    with open(os.path.join(output, 'qa_format.txt'), 'a+',encoding='UTF8') as sa_turn_01:
                        sa_turn_01.write('a\t{}\t{}\n'.format(name, temp_v_a))




                if a_key.lower().startswith('answe'):
                    if '\t' in ' '.join(a_value):
                        name_select.append(name)
                    # with open(os.path.join(output,'qa_info.txt'),'a+',encoding='UTF8') as sav_qa:
                    #     sav_qa.write('{}\t{}\t{}\t{}\t{}\n'.format(name, qas_type, q_detail, a_key+' '+a_value, len(a_value.split(' '))))

                    if not re.findall('answer\s*\d+',a_key.lower()):
                        answer_recode_error.append(a_key)

                if a_key.lower().startswith('relev'):
                    if qas_type == 'Specific Query':
                        part_sav_info['revelant_span'].append('{}\t{}\t{}\t{}\t{}\n'.format(name, qas_type, q_detail, a_key+' '+ ' '.join(a_value), len(' '.join(a_value).split(' '))))
                        temp_min,temp_max = list(set(copy_annotated_qa[name]['all_turn']))[0], list(set(copy_annotated_qa[name]['all_turn']))[-1]
                        relevant_1,relevant2 = False,False
                        if len(a_value) != 1:
                            print('error111',a_value)
                            sys.exit()
                        else:
                            print(a_value[0])
                            if '-' in a_value[0].lower():
                                relevant_1,relevant2 = re.findall('.*?\s*(\d+)\s*-\s*(\d+)\s*',a_value[0])[0]
                            elif '–' in a_value[0].lower():
                                relevant_1,relevant2 = re.findall('.*?\s*(\d+)\s*–\s*(\d+)\s*',a_value[0])[0]
                            else:
                                print('error')
                                sys.exit()
                            # print(relevant_1,relevant2)
                            if int(relevant_1) >= int(temp_min) and int(relevant2) <= int(temp_max):
                                print('turn range---------------:',relevant_1,relevant2,temp_min,temp_max)

                            else:
                                with open(os.path.join(output, 'title_duplicated.txt'), 'a+',encoding='UTF8') as sa_topic:
                                    sa_topic.write('topic span not all in file：{}\t{}\t{}\t{}\t{}\n'.format(name,relevant_1,relevant2,temp_min,temp_max)) 


                    else:
                        print('Specific Query外出现relevant span')
                        sys.exit()

                part_sav_info['sav_pattern'].append('{}\t{}\t{}\t{}\t{}\n'.format(name, qas_type, q_detail, a_key+' '+ ' '.join(a_value), len(' '.join(a_value).split(' '))))

    # single_file_q_info,single_file_a_info
    with open(os.path.join(output,'qa_count.txt'),'a+',encoding='UTF8') as sav_qa_count:
        sav_qa_count.write('{}\t{}\t{}\n'.format(name,len(single_file_q_info),len(single_file_a_info)))

    for sav_content in part_sav_info['sav_pattern']:
        with open(os.path.join(output,'qa_info.txt'),'a+',encoding='UTF8') as sav_qa:
            sav_qa.write(sav_content)

    for sav_span in part_sav_info['revelant_span']:
        with open(os.path.join(output,'qa_span_info.txt'),'a+',encoding='UTF8') as sav_qa_span:
            # sav_qa_span.write(sav_span)
            sav_qa_span.write('{}\t{}\n'.format(len(part_sav_info['revelant_span']),sav_span))
        # print('{}\t{}\t{}\n'.format(name, len(part_sav_info['relevant_span']),sav_span))
    

  


                
#annotated_qa_info -->  {filename :{'Annotated Main Topics': [xx,xx], 'Queries and Annotated Summaries':{
        # General Query: {Q: {a1:xx, a2:xx}, Q: {a1:xx, a2:xx}},
        # Specific Query: {Q: {a1:xx, a2:xx, "Relevent Text Spans":xx }, Q: {a1:xx, a2:xx， "Relevent Text Spans":xx}},
        # Simple Query: {Q: {a1:xx, a2:xx}, Q: {a1:xx, a2:xx}},

print('name select:',name_select)
    # if answer_recode_error:
    #      for single_answer_recode in answer_recode_error:
    #         with open(os.path.join(output, 'qa_format.txt'), 'a+',encoding='UTF8') as sa_turn:
    #             sa_turn.write('{}\t{}\n'.format(name, single_answer_recode))

# line.strip().lower().startswith('question')


    # 'Queries and Annotated Summaries':{
                                # General Query: {Q: {a1:xx, a2:xx}, Q: {a1:xx, a2:xx}},
                                # Specific Query: {Q: {a1:xx, a2:xx, "Relevent Text Spans":xx }, Q: {a1:xx, a2:xx， "Relevent Text Spans":xx}},
                                # Simple Query: {Q: {a1:xx, a2:xx}, Q: {a1:xx, a2:xx}}},
                        #'all_turn': turn_final