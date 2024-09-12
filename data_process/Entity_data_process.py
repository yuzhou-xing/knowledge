import re,os,sys
import shutil,json

def entity_process(inputpath,outputpath):
    folder_content_path = {'wav':[],'txt':[]}
    # pattern = {'DTEST':{'wav':[],'txt':[]},'BTEST':{'wav':[],'txt':[]}}
    pattern = {'DTEST':{},'BTEST':{}}
    ingest_content = {}
    num_matched,num_wav,num_trans = 0,0,0
    for root,dir,files in os.walk(inputpath):
        for file in files:
            if file == 'transcript.txt':
                folder_content_path['txt'].append(os.path.join(root,file))
            elif file.endswith('wav'):
                folder_content_path['wav'].append(os.path.join(root,file))
    print(folder_content_path)
    sys.exit()

    for order,(folder_content_key,folder_content_value) in enumerate(folder_content_path.items()):
        flag_break = False
        for con_path in folder_content_value:  
            data_type = con_path.split('\\')[-2]
            catalog_type = con_path.split('\\')[-4].replace('&','').replace(' ','').replace('_','')
            if catalog_type not in ingest_content.keys():   #eg:{'Banking': {'DTEST':{},'BTEST':{}}}, 'Medical': {'DTEST':{},'BTEST':{}}}
                ingest_content[catalog_type] = pattern

            # print(ingest_content)
            if data_type.upper() not in ingest_content[catalog_type].keys():
                print('错误的文件路径规则:',con_path)
                flag_break = True
                break
            if folder_content_key == 'wav':
                des = os.path.join(outputpath,catalog_type,data_type,'Audio').replace('&','_').replace(' ','')
                if not os.path.exists(outputpath.replace('&','_').replace(' ','')):
                    os.mkdir(outputpath.replace('&','_').replace(' ',''))
                if not os.path.exists(os.path.join(outputpath,catalog_type).replace('&','_').replace(' ','')):
                    os.mkdir(os.path.join(outputpath,catalog_type).replace('&','_').replace(' ',''))
                if not os.path.exists(os.path.join(outputpath,catalog_type,data_type).replace('&','_').replace(' ','')):
                    os.mkdir(os.path.join(outputpath,catalog_type,data_type).replace('&','_').replace(' ',''))
                if not os.path.exists(des):
                    os.mkdir(des)
                shutil.copy(con_path,des)
                num_wav += 1
                ingest_content[catalog_type][data_type.upper()][con_path] = ''
                # print(ingest_content)

            elif folder_content_key == 'txt':
                file_all_trans = Entity_trans(con_path,data_type)
                with open(os.path.join(outputpath,catalog_type,data_type,'transcription.txt').replace('&','_').replace(' ',''),'a+',encoding='UTF8') as trans_sav:
                    for sin_trans in file_all_trans:
                        trans_sav.write(sin_trans+'\n')
                        num_trans += 1
                        for x in ingest_content[catalog_type][data_type.upper()].keys():
                            # print(sin_trans.split('\t')[0],os.path.splitext(os.path.basename(x))[0])
                            if sin_trans.split('\t')[0] == os.path.basename(x):# and not ingest_content[catalog_type][data_type.upper()][x]:
                                ingest_content[catalog_type][data_type.upper()][x] = sin_trans
                                # print('====================',sin_trans.split('\t')[0])
                                num_matched += 1
        
                #--------------------------------------------------------------------------------
                with open(os.path.join(outputpath,'Carbon_input.txt').replace('&','_').replace(' ',''),'a+',encoding='UTF8') as trans_sav_all:
                    for sin_trans in file_all_trans:
                        flag_1 = False
                        for single_wav in folder_content_path['wav']:
                            if sin_trans.strip().split('\t')[0] in single_wav:
                                trans_sav_all.write(single_wav +'\t'+ sin_trans.strip().split('\t')[1] +'\n')
                                flag_1 = True
                        
                        if not flag_1:
                            print('未找到音频完整路径:',sin_trans.strip().split('\t')[0])
                            sys.exit()
                #--------------------------------------------------------------------------------
                        

        if flag_break:
            break

    print('matched wav和trans count:',num_matched,'wav count:',num_wav,'trans count:',num_trans)  #{cata:{'DTEST':{'wav':[],'txt':[]},'BTEST':{'wav':[],'txt':[]}}}
    for order_j,(k_j,v_j) in enumerate(ingest_content.items()):
        if len(ingest_content[k_j]['BTEST']) != len([x for x in ingest_content[k_j]['BTEST'].values() if x.strip() != '']):
            print(ingest_content[k_j]['BTEST'])
            print([x for x in ingest_content[k_j]['BTEST'].values() if x.strip() != ''])
            print('{}:{}音频数大于trans数,实际：{}'.format(k_j,'BTEST',len([x for x in ingest_content[k_j]['BTEST'].values() if x.strip() != ''])))
        if len(ingest_content[k_j]['DTEST']) != len([x for x in ingest_content[k_j]['DTEST'].values() if x.strip() != '']):
            print('{}:{}音频数大于trans数,实际：{}'.format(k_j,'DTEST',len([x for x in ingest_content[k_j]['DTEST'].values() if x.strip() != ''])))
        print('{}: BTEST count:{}\t DTEST count:{}\n'.format(k_j,len(ingest_content[k_j]['BTEST']),len(ingest_content[k_j]['DTEST'])))

    with open(os.path.join('\\'.join(outputpath.split('\\')[:-1]),outputpath.split('\\')[-1]+'.json'),'w',encoding='UTF8') as sav_j:
        json.dump(ingest_content,sav_j,ensure_ascii=False,indent=4)





def Entity_trans(inputpath,test_type):
    single_trans,transcription_line_count,wav_count,save_wav_count,catalog_type = [],0,[],[],{}   
    count = 0
    all_trans = []
    single_dict = {}
    with open(inputpath,'r',encoding='UTF8') as f_trans:
        for i,line in enumerate(f_trans):
            file_wav_name = '_'.join(os.path.splitext(line.split('\t')[0].strip())[0].split('_')[:-1]).replace('\ufeff','')
            seg_ID = os.path.splitext(line.split('\t')[0].strip())[0].split('_')[-1]

            if file_wav_name not in single_dict.keys():
                single_dict[file_wav_name] = {int(seg_ID):line.split('\t')[1].strip()} #line.split('\t')[1].strip()
            elif int(seg_ID) not in single_dict[file_wav_name].keys():
                single_dict[file_wav_name][int(seg_ID)] = line.split('\t')[1].strip()
            else:
                print('segmentID 重复')

            if test_type not in catalog_type.keys():
                catalog_type[test_type] = []
            catalog_type[test_type].append(file_wav_name)

            count = i
    for j,(key_ind,v_ind) in enumerate(single_dict.items()):
        sav_single_trans = ''

        if sorted(v_ind) != [x for x in v_ind.keys()]:
            print('original transcription file: segment ID disorder: {} {}\n乱序{}\t保存顺序{}\n'.format(test_type,key_ind,[x for x in v_ind.keys()],sorted(v_ind)))
        if diff_list(sorted(v_ind)):
            print('有缺省的segment ID')
        for ind_k in sorted(v_ind):
            sav_single_trans = '{} {}'.format(sav_single_trans,v_ind[ind_k])
        all_trans.append('{}{}\t{}'.format(key_ind,'.wav',sav_single_trans)) 
        sav_single_trans = ''
    return all_trans

        # if not os.path.exists(os.path.join(outputpath,'refine_input')):
        #     os.mkdir(os.path.join(outputpath,'refine_input'))

        # with open(os.path.join(os.path.join(outputpath,'refine_input'),'carbon_input_{}.txt'.format(test_type)),'a+',encoding='UTF8') as sav:
        #     sav.write('{}\t{}\n'.format(os.path.join(wav_path_part,key_ind+'.wav'),sav_single_trans.strip()))
        # with open(os.path.join(os.path.join(outputpath,'refine_input'),'carbon_input.txt'),'a+',encoding='UTF8') as sav:
        #     sav.write('{}\t{}\n'.format(os.path.join(wav_path_part,key_ind+'.wav'),sav_single_trans))

#     save_wav_count.extend(single_dict.keys())


# print('浏览得到wav个数{}，保存wav个数{},浏览-保存={}，保存-浏览={}'.format(len(wav_count),len(save_wav_count),set(wav_count) - set(save_wav_count),set(save_wav_count) - set(wav_count)))
# print('Btest保存了:{}文件，{}行,Dtest保存了:{}文件，{}行'.format(len(set(catalog_type['BTest'])),len(catalog_type['BTest']),len(set(catalog_type['DTest'])),len(catalog_type['DTest'])))

def segID_sort():

    return 
def diff_list(input_list):
    for order,con in enumerate(input_list):
        if order < len(input_list) - 1:
            if abs(int(con)-int(input_list[order+1])) != 1:
                return True
    return False

def check_first_alpha_isupper_and_isLegelDot(filepath,line):
    EndFlag = ['.','?','!']
    content_list = line.split(' ')
    for i,word in enumerate(content_list):
        if i < len(content_list) - 1:
            for j,letter in enumerate(list(word)):
                if len(set(EndFlag) - set(list(word))) != 3:
                    if len(set(EndFlag)-(set(EndFlag) - set(list(word)))) == 1 and word[-1] == set(EndFlag)-(set(EndFlag) - set(list(word))):   #need check type
                        pass
                        
    

entity_process(sys.argv[1],sys.argv[2])   #输入文件到最后应该是分文件的一级