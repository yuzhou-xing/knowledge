import re
import os

'''
    # <NE></NE>  <NE:name></NE:name>
    # tag_pattern = r"<NE:.*[^>]*>(.*?)</NE:.*>"
    # tag_pattern_ne = r"(<NE:.*?[^>]*>.*?</NE:.*?>)"
    tag_pattern_nename = r"(<NE:.*?[^>]*>.*?</NE:.*?>)"   # 非贪婪模式
    tag_pattern_ne = r"(<NE?[^>^:]*>.*?</NE>)"

    trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en>for<NE:name>be</NE:name><NE>re</NE></FW:en>tools"
    trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en>a<NE:name></NE:name><NE>re</NE></FW:en>tools"
    trans = "Be these<NE:name>restr other</NE:name>supersonicvery<FW:en>a<NE:name></NE:name></FW:en>tools"
    trans = "Be theserestr<NE>restr</NE>d othersupersonic<NE>re</NE>very<FW:en>a<NE>re</NE></FW:en>tools"
    trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en>a<NE:name></NE:name><NE>re</NE></FW:en>tools"
    trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en>a<NE:name></NE:name><NE>re</NE></FW:en>tools"
    trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supers</FW:en>onic<NE>re</NE>very<FW:en>a<NE:name></NE:name><NE>re</NE></FW:en>tools"
    trans = "Be these supersonic very<FW:en>a asdfa f asdf<FW:en> asdf </FW:en>adsf asdf </FW:en>tools"

    <NE></NE>   <NE:name></NE:name>  <FW:en></FW:en>
    已完成验证规则：
        1.首先检查是否存在不成对的情况（极限情况：<NE>abc<NE:name>bcd<NE>adsfasdf</NE></NE:name>d other</NE> 这种情况也算不合法）
        2.相同标签不可嵌套，不同标签可以嵌套(仅限于<NE:name>adsf<NE>adf</NE></NE:name>)
        3.如果标签包含空内容， 或者标签内词数大于某个值(此时定的words 个数为 10, 可调),时， 不合法
        4.<NE><NE:name>abcdefg</NE:name></NE>   这种情况也算<NE></NE>包含空内容，不合法
        5.只有 <NE> 以及 <NE:name>  (只存在<NE> 或者 <NE:name> 不合法)
        6.只有<FW:en>   同样不允许空内容或者包括单词数大于阈值
        7. 5 和 6 混合都有  检测规则同上方规则
'''

def getAlltags(trans_info):
    # patterns = ['OVERLAP', 'OL', 'PName', 'NIS','overlap', 'NE',"NE:.*?"]
    # <FW:en></FW:en>
    patterns = ['NE',"NE:.*?","FW:en"]
    logs = []
    for pattern in patterns:
        # 三种情况，eg: <EN/> or </EN>
        # 检查项：1：是否成对，2：是否存在相同标签之间嵌套 eg:<NE><NE></NE></NE>， 3，标签中token个数限制
        res1 = re.search(r'[<\[\(]{}/[>\]\)]'.format(pattern), trans_info) #search as: <NE>
        if res1 is not None:
            continue
        pp = r'[<\[\(]/?{}[>\]\)]'.format(pattern)  #search as: </NE> or <NE>
        res2 = re.findall(pp, trans)
        flag = True
        if len(res2) % 2 >0:  # single tag, 是否成对
            flag = False
        else:
            last = None
            for i, o1 in enumerate(res2):
                if i == 0 and '/' in o1:  #the first tag such <NE/> or </NE>
                    flag = False
                if last and last == o1:    #no tag or overlap(嵌套)
                    flag = False
                last = o1 
        if not flag:
            logs.append(pattern)
    tag_check_res=list(set(logs))
    if tag_check_res:
        print("list of unnormal labels",tag_check_res)
        return False
    else:
        return True
    
def check_blank_too_many(trans,tags):
    if not trans.strip():
        print(f"{tags} contains blank content")
        return False
    elif len(trans.strip().split(" ")) > 10:
        print(f"{tags} contains btoo many words")
        return False
    else:
        return True
    
def check_paire_tags(trans):  #检查配对tag
    trans_format = getAlltags(trans)
    if not trans_format:
        return trans_format
    tag_pattern_nename = r"(<NE:.*?[^>]*>.*?</NE:.*?>)"   # 非贪婪模式
    tag_pattern_ne = r"(<NE?[^>^:]*>.*?</NE>)"
    tag_pattern_fw = r"(<FW:en?[^>^:]*>.*?</FW:en>)"
    res_nename = re.findall(tag_pattern_nename,trans)
    res_ne = re.findall(tag_pattern_ne,trans)
    res_fw = re.findall(tag_pattern_fw,trans)

    # 首先排除单独 NE NE:name 出现的情况
    if (res_nename and not res_ne) or (not res_nename and res_ne):
        #print("<NE></NE> and <NE:name></NE:name> must either occur simultaneously or not occur simultaneously.")
        return True
    
    # 只有fw标签
    if not res_nename and not res_ne:
        if res_fw:
            for fwt in re.findall(r"<FW:en?[^>^:]*>(.*?)</FW:en>",trans):
                if not check_blank_too_many(fwt,"<FW:en></FW:en> "):
                    return False
            return True
        else:
            return True
        
    else:
        if not res_fw:
            # 1.检查是否嵌套 2.检查标签内文本words个数
            ne_in_nename = False
            for rnn in res_nename:
                if re.findall(tag_pattern_ne,rnn):
                    ne_in_nename = True
                    break
            if ne_in_nename:
                # 检查的时候多一步判断
                temp_resrn = re.findall(r"<NE?[^>^:]*>(.*?)</NE>",trans)
                for trn in temp_resrn:
                    if not check_blank_too_many(trn,"<NE></NE> "):
                        print('if not check_blank_too_many(trn,"<NE></NE> ")')
                        return False
            temp_trans = re.sub(tag_pattern_ne,"",trans)
            temp_res_rnn = re.findall(r"<NE:.*?[^>]*>(.*?)</NE:.*?>",temp_trans)
            for trnn in  temp_res_rnn:
                if not check_blank_too_many(trnn,"<NE:name></NE:name> "):
                    print('if not check_blank_too_many(trnn,"<NE:name></NE:name> "):')
                    return False        
            nename_in_ne = False
            for rn in res_ne:
                if re.findall(tag_pattern_nename,rn):
                    nename_in_ne = True
                    break
            if nename_in_ne:
                print("1_not allow <NE>adf<NE:name>adsf</NE:name></NE>")
                return False
            temp_trans = re.sub(tag_pattern_nename,"",trans)
            temp_res_rnn = re.findall(r"<NE[^>]*>(.*?)</NE>",temp_trans)
            for trnn in  temp_res_rnn:
                if not check_blank_too_many(trnn,"<NE></NE> "):
                    print('if not check_blank_too_many(trnn,"<NE></NE> "): 130')
                    return False
            return True
        else:
            # 三者都有，只要保证FW:en标签中文本满足不为空且单词数量不超过10即可
            for temp_fw_t in res_fw:
                temp_fw_t = re.sub(tag_pattern_nename,"",temp_fw_t)
                temp_fw_t = re.sub(tag_pattern_ne,"",temp_fw_t)
                temp_fw_t_info = re.findall(r"<FW:en?[^>^:]*>(.*?)</FW:en>",temp_fw_t)
                for item in temp_fw_t_info:
                    if not check_blank_too_many(item,"<FW:en></FW:en> "):
                        print('if not check_blank_too_many(item,"<FW:en></FW:en> "): 141')
                        return False
            # 需要删除掉所有FW标签的内容，如果内部嵌套其他标签，则保留
            raw_trans = trans
            tag_pattern_fw_new = r"(<FW:en?[^>^:]*>(.*?)</FW:en>)"
            new_fw_res_list = re.findall(tag_pattern_fw_new,trans)
            for item in new_fw_res_list:
                top_f = item[0]
                top_s = item[1]
                is_deal = re.findall(r"<[^>].*>",top_s)
                if is_deal:
                    raw_trans = raw_trans.replace(top_f,is_deal[0])
                else:
                    raw_trans = raw_trans.replace(top_f,"")
            
            # 1.检查是否嵌套 2.检查标签内文本words个数
            ne_in_nename = False
            for rnn in res_nename:
                if re.findall(tag_pattern_ne,rnn):
                    ne_in_nename = True
                    break
            if ne_in_nename:
                # 检查的时候多一步判断
                temp_resrn = re.findall(r"<NE?[^>^:]*>(.*?)</NE>",raw_trans)
                for trn in temp_resrn:
                    if not check_blank_too_many(trn,"<NE></NE> "):
                        print('if not check_blank_too_many(trn,"<NE></NE> "): 167')
                        return False
            temp_trans = re.sub(tag_pattern_ne,"",raw_trans)
            temp_res_rnn = re.findall(r"<NE:.*?[^>]*>(.*?)</NE:.*?>",temp_trans)
            for trnn in  temp_res_rnn:
                if not check_blank_too_many(trnn,"<NE:name></NE:name> "):
                    print('if not check_blank_too_many(trnn,"<NE:name></NE:name> "): 173')
                    return False        
            nename_in_ne = False
            for rn in res_ne:
                if re.findall(tag_pattern_nename,rn):
                    nename_in_ne = True
                    break
            if nename_in_ne:
                print("2_not allow <NE>adf<NE:name>adsf</NE:name></NE>")
                return False
            temp_trans = re.sub(tag_pattern_nename,"",raw_trans)
            temp_res_rnn = re.findall(r"<NE[^>]*>(.*?)</NE>",temp_trans)
            for trnn in  temp_res_rnn:
                if not check_blank_too_many(trnn,"<NE></NE> "):
                    print('if not check_blank_too_many(trnn,"<NE></NE> "):186' )
                    return False
            return True
    
if __name__ == "__main__":
    print("beginning....")

    # trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en>for<NE:name>be</NE:name><NE>re</NE></FW:en>tools"
    # trans = "Be these<NE:name>restrrestrd other</NE:name>super<NE>sonicv</NE>ery<FW:en>for<NE:name>be</NE:name></FW:en>tools"
    # trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en><NE:name></NE:name><NE>re</NE></FW:en>tools"

    # trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en>a a a a a a a a a a a a a a a a<NE:name></NE:name><NE>re</NE></FW:en>tools"

    # trans = "Be these<NE:name>restr other</NE:name>supersonicvery<FW:en>a<NE:name>ads</NE:name></FW:en>tools"
    # trans = "Be theserestr<NE>restr</NE>d othersupersonic<NE>re</NE>very<FW:en>a<NE>re</NE></FW:en>tools"  # only NE
    # trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en><NE:name>asd</NE:name><NE>re</NE></FW:en>tools"
    #trans = "Auf dem Lebensmittelbereich und natürlich <FILL/> vor einigen wochen auf diese pipeline dort <FILL/> und das ist der gute Aufruf auch an die Banken aufzupassen denn auch dort hat man ja Daten <FILL/>."
    # trans = "Be these supersonic very<FW:en>a<NE:name>a</NE:name></FW:en>tools"
    # trans = "Be these <FW:en> asdf </FW:en> supersonic very<FW:en>a asdfa f asdfadsf asdf </FW:en>tools"

    # getAlltags(trans)
    # print(check_paire_tags(trans))

    # bad_list = []
    # bad_n_list = []
    # bp = r"E:\v-feiyuzhang\20230724_taskdata\en-US"
    # json_list = []
    # for r,d,fs in os.walk(bp):
    #     for f in fs:
    #         if f.endswith(".txt"):
    #             json_list.append(os.path.join(r,f))
    # for tp in json_list:
    #     with open(tp,'r',encoding="utf-8") as fr:
    #         lines = fr.readlines()
    #         for line in lines:
    #             trans = line.split("\t")[1].strip()
    #             res = check_paire_tags(trans)
    #             if not res:
    #                 bad_n_list.append(tp)
    #                 bad_list.append(f"{tp}\t{trans}\n")
    #                 # break
    # print(len(set(bad_n_list)),len(json_list))
    # with open(r"E:\v-feiyuzhang\20230724_taskdata\res_en-US.tsv",'w',encoding="utf-8") as fw:
    #     for b in bad_list:
    #         fw.write(b)

    import sys
    bad_list = []
    bad_n_list = []
    bp = sys.argv[1]
    json_list = []
    for r,d,fs in os.walk(bp):
        for f in fs:
            if f.endswith(".txt"):
                json_list.append(os.path.join(r,f))
    for tp in json_list:
        print(tp)
        with open(tp,'r',encoding="utf-8") as fr:
            lines = fr.readlines()
            for line in lines:
                trans = line.split("\t")[1].strip()

                #tsv trans
                #f_p,s_p = line.strip().split(']',1)
                #trans = s_p.strip().split(' ',1)[1]

                res = check_paire_tags(trans)
                if not res:
                    bad_n_list.append(tp)
                    bad_list.append(f"{tp}\t{trans}\n")
                    # break
    print(len(set(bad_n_list)),len(json_list))
    print(set(bad_n_list),json_list)
    if bad_list:
        with open(os.path.join(sys.argv[2],"verify_tag.txt"),'a+',encoding="utf-8") as fw:
            for b in bad_list:
                fw.write(b)

