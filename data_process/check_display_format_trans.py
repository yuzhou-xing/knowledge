import os,re,sys

#用Placeholder替换空格并在没有与word分隔开的tag周围加空格

def list_trans(trans):
    flag = False   
    some_Placeholder = [',','!',';','#','@','&','*','^','+','?']
    for Placeholder in some_Placeholder:
        if Placeholder not in trans and ' ' in trans:
            trans_pro = trans.replace(' ',Placeholder)
            flag = True
            break

    if flag == True:
        trans_pro = list(trans_pro)
        for i,letter in enumerate(trans_pro):
            if '[' == letter and trans_pro[i-1] != ' ':
                trans_pro.insert(i,' ')
            if i != len(trans_pro)-1:       #防止list index out of range
                if ']' == letter and trans_pro[i+1] != ' ':
                    trans_pro.insert(i+1,' ')
        # trans_pro = ''.join(trans_pro).replace(Placeholder,' ')
        return Placeholder,''.join(trans_pro)  #like: , | Be,these <NE:name> restr <NE> restr </NE> d,other </NE:name> supers,onic <NE> re </NE> very <FW:en> a <NE:name> </NE:name> <NE> re </NE> </FW:en> tools
    else:
        return False,''.join(trans)

def check_display_trans(Placeholder,trans):

    #insert tag周围相连内容为空格
    # trans = 
    #检查括号
    # check_brackets
    all_response_brackets = re.findall('\[.*?\]',trans)
    # print(all_response_brackets)

    #左右括号不匹配.
    for i in all_response_brackets:
        if i.count('[') + i.count(']') != 2:
            print('左右括号不匹配')
            return False,'左右括号不匹配'

    bracket_dict = {}
    contentDelBracket_dict = {}
    for i,part in enumerate(trans.split(' ')):
        if part in all_response_brackets:
                bracket_dict[i] = part
        else:
            contentDelBracket_dict[i] = part
    # print(bracket_dict,'\n',contentDelBracket_dict)

    # trans_replace = trans
    # for i in all_response_brackets:
    #     trans_replace = trans_replace.replace(i,'',1)
    # print('trans_replace----',trans_replace)
    # if '[' in trans_replace or ']' in trans_replace:
    #     print('左右括号未完全匹配')
    #     return False
    

    for i,(k_bracket,bracket) in enumerate(bracket_dict.items()):
        bracket_content = bracket.split('[')[1].split(']')[0]
        # print(bracket_content)
        if Placeholder:
            if  len(bracket_content.replace(Placeholder,' ').strip()) == 0:
                print('括号中为空')
                return False,'括号中为空'

        # | 左右索引不为空
        if '|' in bracket_content:
            for index,char in enumerate(bracket_content):
                if '|' == char:
                    try:
                        if bracket_content[index-1] and bracket_content[index+1]:  #####
                            pass
                    except:
                        print('list out of range error')
                        return False,'list out of range error'
            if len(bracket_content.split('|')) != len(set(bracket_content.split('|'))):
                print('括号内符号重复')
                return False,'括号内符号重复'
                
        else:
            if len(bracket_content) != 1:
                print("括号内容的错误写法(不包含|且为多个字符)")
                return False,'括号内容的错误写法(不包含|且为多个字符)'
        if i != len(bracket_dict) -1:
            for j,(k,v) in enumerate(bracket_dict.items()):
              #  if i != len(bracket_dict) -1:
                if abs(k_bracket - k) == 1:
                    print('两个括号相连')
                    return False,'两个括号相连'
                elif abs(k_bracket - k) == 2 and len(contentDelBracket_dict[(k_bracket+k)/2].replace(Placeholder,'').strip()) == 0:
                    print('两个括号相连')
                    return False,'两个括号相连'
    return True,None

def judge_timestamp_with_lexical(display_line,lexical_line):
    pass

# display_root,lexical_root = '',''
# display_file,lexical_file,error_file = [],[],[]
# display_dict,lexical_dict = {},{}
# for root,der,files in os.walk(sys.argv[1]):
#     ##默认是speech ocean的带时间戳格式的数据,tsv format
#     flag = set()    

#     #judge xidisplay folder和lexical folder的文件相互对应，且为一个文件夹中文件
#     for i,file in enumerate(files):
#         if root.split('\\')[-1] == 'display_transcriptions' and file.endswith('tsv'):
#             if display_root == '':
#                 display_root = root
#             elif root != display_root:
#                 print('超过一个display_transcriptions文件夹')
#             display_file.append(file)
#         elif root.split('\\')[-1] == 'lexical_transcriptions' and file.endswith('tsv'):
#             if lexical_root == '':
#                 lexical_root = root
#             elif root != lexical_root:
#                 print('超过一个lexical_transcriptions文件夹')
#             lexical_file.append(file)

# if sorted(display_file) == sorted(lexical_file):
#     print('display file and lexical file match, contain {}'.format(len(display_file)))
#     for one_file in display_file:
#         ##########################检查括号和时间戳以及行是否对应####################
#         with open(os.path.join(display_root,one_file),'r',encoding='UTF8') as f_display,open(os.path.join(lexical_root,one_file),'r',encoding='UTF8') as f_lexical:
#             lexical_content = f_lexical.readlines()
#             # display_content = f_display.readlines()
#             for line_index,line_display in enumerate(f_display):
#                 # if line_index == 0 and re.findall('\[\d+\.\d+ \d+\.\d+\] \w\d ',line_display):
#                 if line_index == 0 and re.findall('\[\d+\.\d+ \d+\.\d+\] [sS]\d ',line_display):
#                     print(line_display)
#                     # if line_display.strip() != '' and line_index :
#                     #     display_line_count 
                    
#                     trans = line_display.split(']',1)[1].strip().split(' ',1)[1].strip()
#                     Placeholder, trans_pro=list_trans(trans)
#                     return_flag = check_display_trans(Placeholder, trans_pro)
#                     if not return_flag:
#                         print(one_file,line_display)
#                         error_file.append('{}\t{}',one_file,line_display)
#                     flag.add('format1')

#                     display_timestamp = line_display.split(']')[0].strip()+']'
#                     lexical_timestamp = lexical_content[line_index].split(']')[0].strip()+']'
#                     if display_timestamp != lexical_timestamp:
#                         print('lexical和display文件的timestamp 不对应')
#                         print(line_display)
#                         print(lexical_content[line_index])

#                 else:  #tsv file not contain speakerID
#                     trans = line_display.split(']',1)[1].strip()
#                     # print(trans)
#                     Placeholder, trans_pro=list_trans(trans)
#                     return_flag = check_display_trans(Placeholder, trans_pro)
#                     if not return_flag:
#                         print(one_file,line_display)
#                         error_file.append('{}\t{}'.format(one_file,line_display))
#                     flag.add('format2')

#                     display_timestamp = line_display.split(']')[0].strip()+']'
#                     lexical_timestamp = lexical_content[line_index].split(']')[0].strip()+']'
#                     if display_timestamp != lexical_timestamp:
#                         print('lexical和display文件的timestamp 不对应')
#                         print('display_timestamp:',display_timestamp,'lexical_timestamp:',lexical_timestamp,len(list(display_timestamp)),len(list(lexical_timestamp)))
#                         print(line_display)
#                         print(lexical_content[line_index])
#                         # set(list(display_timestamp))-set(list(lexical_timestamp))
#             #verify
#             # if len([con for con in lexical_content if con.strip() != '']) != len([con_1 for con_1 in display_content if con_1.strip() != '']):
#             #     # print(con)
#             #     print("lexical和display行数不对应",one_file)
# else:
#     print('display和lexical文件mismatch')
# for error_line in error_file:
#     with open(os.path.join(sys.argv[1],'error_file.txt'), 'a+', encoding='UTF8') as sav:
#         sav.write(error_line)


#         if file.endswith('tsv'):
#             with open(os.path.join(root,file),'r',encoding='UTF8') as f:
#                 for i, line in enumerate(f):
#                     if i == 0 and re.findall('\[\d+\.\d+ \d+\.\d+\] \w\d ',line):
#                         trans = line.split(']',1)[1].strip().split(' ',1)[1].strip()
#                         Placeholder, trans_pro=list_trans(trans)
#                         return_flag = check_display_trans(Placeholder, trans_pro)
#                         if not return_flag:
#                             print(file,line)
#                             error_file.append('{}\t{}',file,line)
#                         flag.add('format1')
                    
#                     else:
#                         trans = line.split(']',1)[1].strip()
#                         Placeholder, trans_pro=list_trans(trans)
#                       
#   return_flag = check_display_trans(Placeholder, trans_pro)
#                         if not return_flag:
#                             print(file,line)
#                             error_file.append('{}\t{}'.format(file,line))
#                         flag.add('format2')
# for error_line in error_file:
#     with open(os.path.join(sys.argv[1],'error_file.txt'), 'a+', encoding='UTF8') as sav:
#         sav.write(error_line)


#debug code
# trans = 'Můj oblíbený film je Interstellar[,| ]    [ |,]  sci fi film z roku 2014 režiséra Christophera Nolana[.] Film sleduje tým astronautů[,] kteří se vydávají na misi s cílem najít novou obyvatelnou planetu pro lidstvo poté[,| ] co se Země stává stále více neobyvatelnou kvůli klimatickým změnám a globální potravinové krizi[.]'
# Placeholder, trans_pro=list_trans(trans)
# check_display_trans(Placeholder, trans_pro)