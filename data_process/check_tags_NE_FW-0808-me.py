import re,os

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
#用Placeholder替换空格并在没有与word分隔开的tag周围加空格
def list_trans(trans):
    flag = False   
    some_Placeholder = [',','!',';','#','@','&','*','^','+','?']
    for Placeholder in some_Placeholder:
        if Placeholder not in trans and ' ' in trans:
            trans_pro = trans.replace(' ',Placeholder)
            flag = True
            break
        else:
            trans_pro = trans

        
    # print(trans)
    trans_pro = list(trans_pro)
    #print(trans)
    for i,letter in enumerate(trans_pro):
        if '<' == letter and trans_pro[i-1] != ' ':
            trans_pro.insert(i,' ')
        if i != len(trans_pro)-1:       #防止list index out of range
            if '>' == letter and trans_pro[i+1] != ' ':
                trans_pro.insert(i+1,' ')
    # print('list_trans_add_space:',''.join(trans_pro))
    if flag == True:
        return Placeholder,''.join(trans_pro)  #like: , | Be,these <NE:name> restr <NE> restr </NE> d,other </NE:name> supers,onic <NE> re </NE> very <FW:en> a <NE:name> </NE:name> <NE> re </NE> </FW:en> tools
    else:
        return False,''.join(trans_pro)

def check_paire_tags(placeholder,trans):
    #这里输入的trans是空格替换过tag周围无空格之后的数据
    # all_content_list = re.split(r' |{}'.format(placeholder),trans)
    all_content_list = trans.split(' ')

    #由于之前将空格替换为占位符，所以删除tag后，列表中的一个元素就是tag包含的内容
    # content_delTag = [x for x in all_content_list if "<" not in x and '>' not in x]
    
    correct_tag= ['<NE>', '</NE>', '<NE:name>', '</NE:name>', '<FW:en>', '</FW:en>']   
    all_tag = re.findall('<.*?>',trans)
    # print('all_tag:',all_tag)
    # print('all_content_list:',all_content_list)

    #替换掉trans中的<.*?>, 检查是否有未闭合的tag
    replace_tag_trans = re.sub('<.*?>',' ',trans)
    if '<' in replace_tag_trans or '>' in replace_tag_trans:
        print('未闭合标签')
        return False


    #在此替换all_tag只是想查看未闭合标签的范围广一些
    all_tag = [x for x in all_tag if x in correct_tag]

    if len(all_tag)%2:
        print('标签不成对')
        return False
 
    part_content = False
    tag_dict = {}
    contentDelTag_dict = {}
    for i,part in enumerate(all_content_list):
        # for match in re.finditer('<.*?>', all_content_list):
        #     print(match.group(), match.start(), match.end())
        if part in correct_tag:
                tag_dict[i] = part
        else:
            contentDelTag_dict[i] = part
    # print(tag_dict,'\n',contentDelTag_dict)

    #tag
    flag = True
    corresponding_tag = []
    for i,(k,v) in enumerate(tag_dict.items()):

        if v in correct_tag:
            if i == 0 and '/' in v:
                print('错误标签开头')
                return False
            if i == len(tag_dict)-1 and '/' not in v:
                print(v)
                print('错误标签结尾')
                return False
            # if len(all_tag)%2:
            #     print('标签不成对')
            #     return False
            if '/' not in v:   #只找左标签
                tag_content = v.replace('<','').replace('>','')
                #
                pair_and_include_tag = ''
                for i_cir,(k_cir,v_cir) in enumerate(tag_dict.items()):

                    #对应的右标签
                    if i_cir > i and '</{}>'.format(tag_content) == v_cir:
                        # print(k,k_cir)
                        #一对tag及其包含的其他tag
                        pair_and_include_tag =[x for j,x in tag_dict.items() if (k <= j <= k_cir)]  

                        #一对tag list  ===========================verify=====================================
                        corresponding_tag.append([k,v,k_cir,v_cir])


                        if len(pair_and_include_tag) != len(set(pair_and_include_tag)):
                            print('相同tag嵌套')
                            return False
                        
                        #包含在一对标签中的word list
                        contentDelTag_include = [contentDelTag_value for num,contentDelTag_value in contentDelTag_dict.items() if k < num < k_cir]

                        if placeholder:
                            content_include_join = ' '.join(contentDelTag_include).replace(placeholder,' ')
                        else: 
                            content_include_join = ' '.join(contentDelTag_include)
                        content_word_len = content_include_join.count(content_include_join)
                        if content_word_len > 10 or content_include_join.strip() == '':
                            print('标签中word > 10个或一对标签中内容为空')
                            return False
                        break
                #判定找不到右标签的情况
                if i_cir == len(tag_dict)-1 and pair_and_include_tag == '':
                    print('没有找到右标签',k,v)
                    return False
                    
        else:
            print('不正确或大小写问题的标签或other TAG:',v)

            return False


    print('corresponding_tag:',corresponding_tag)

    for i,tag_response in enumerate(corresponding_tag):
        if i == len(corresponding_tag)-1:
            break
        if abs(int(corresponding_tag[i+1][0])-int(tag_response[0])) == 1 and abs(int(corresponding_tag[i+1][2])-int(tag_response[2])) == 1:
            print('形如以下情况的 <NE>/NE>包围空，<NE><NE:name>abcdefg</NE:name></NE>')
            return False
    return True
    


    
if __name__ == "__main__":
    print("beginning....")

    trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en>for<NE:name>be</NE:name><NE>re</NE></FW:en>tools"
    # trans = "Be these<NE:name>restrrestrd other</NE:name>super<NE>sonicv</NE>ery<FW:en>for<NE:name>be</NE:name></FW:en>tools"
    trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en><NE:name></NE:name><NE>re</NE></FW:en>tools"

    trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en>a a a a a a a a a a a a a a a a<NE:name></NE:name><NE>re</NE></FW:en>tools"

    # trans = "Be these<NE:name>restr other</NE:name>supersonicvery<FW:en>a<NE:name>ads</NE:name></FW:en>tools"
    # trans = "Be theserestr<NE>restr</NE>d othersupersonic<NE>re</NE>very<FW:en>a<NE>re</NE></FW:en>tools"  # only NE
    # trans = "Be these<NE:name>restr<NE>restr</NE>d other</NE:name>supersonic<NE>re</NE>very<FW:en><NE:name>asd</NE:name><NE>re</NE></FW:en>tools"
    trans = "Be these<NE><NE:name>res trrestr d other</NE:name></NE>supers       onic<NE>re</NE>very<FW:en>a<NE:name>sd</NE:name><NE>re</NE></FW:en>tools"
    # trans = "Be these supersonic very<FW:en>a<NE:name>a</NE:name></FW:en>tools"
    # trans = "Be these <FW:en> asdf </FW:en> supersonic very<FW:en>a asdfa f asdfadsf asdf </FW:en>tools"
    #trans = "Benvenuti su <NE> medicina e <NE>informazione Web T. V. </NE>, il <NE> trapianto</NE> d'organo </NE> è una fra le più importanti conquiste della scienza e della <NE> medicina </NE>."



    # placeholder,trans_pro = list_trans(trans)
    # print(check_paire_tags(placeholder,trans_pro))


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
        with open(tp,'r',encoding="utf-8") as fr:
            lines = fr.readlines()
            for line in lines:
                trans = line.split("\t")[1].strip()
            
                #tsv trans
                #f_p,s_p = line.strip().split(']',1)
                #trans = s_p.strip().split(' ',1)[1]
            
                # trans = line.split("\t")[1].strip()
                if '/' in re.sub('<.*?>','',trans):
                    print(tp)
                    print(line.split("\t")[0])



                placeholder,trans_pro = list_trans(trans)
                res = check_paire_tags(placeholder,trans_pro)
                # res = check_paire_tags(trans)
                if not res:
                    bad_n_list.append(tp)
                    bad_list.append(f"{tp}\t{trans}\n")
                    # break
    print(len(set(bad_n_list)),len(json_list))
    print(set(bad_n_list),json_list)
    if bad_list:
        with open(os.path.join(sys.argv[2],"verify_tag1.txt"),'a+',encoding="utf-8") as fw:
            for b in bad_list:
                fw.write(b)
        

    
    

    
