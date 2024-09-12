
#算两次WER, 两个方法都用, 其中在输入路径文件结构以及文件文本内容不同有可能造成报错或写入文件错误

import os,librosa,random,shutil,csv,sys
from concurrent.futures import ThreadPoolExecutor
import wave
def chcek_audio_framerate_wave_new(w_p):
    try:
        count = 0
        sum_wav = 0
        def get_wav_info(wav_path):
            try:
                audio_info = wave.open(wav_path,mode="rb")
                params = audio_info.getparams()
                nchannels,sampwidth,framerate,nframes = params[:4]
                duration = nframes / framerate
                return (framerate,duration,nchannels)
            except Exception as e:
                print(wav_path)
                print(e)
                return (0,0,0)
        samplerate_list = []
        nchannels_list = []
        wp_info_list = []
        for root, dirs, files in os.walk(w_p):
            for name in files:
                if name.split('.')[-1] in ['WAV','wav']:
                    wp_info_list.append(os.path.join(root,name))

        with ThreadPoolExecutor(100) as pool:
            result = pool.map(get_wav_info,wp_info_list)
        
        for res in result:
            if res[0] not in samplerate_list:
                samplerate_list.append(res[0])
            if res[-1] not in nchannels_list:
                nchannels_list.append(res[-1])
            count += res[1]

        sum_wav = len(wp_info_list)
        
        print({'wav_count':sum_wav,'total_duration':count/3600,'samplerate':samplerate_list,"nchannels_list":nchannels_list,"wav_path":w_p})
        return {'wav_count':sum_wav,'total_duration':round(count/3600,2),'samplerate':samplerate_list,"nchannels_list":nchannels_list}

    except Exception as e:
        print(e)
        return False


def get_duration(p):
    t = 0
    try:
        t = librosa.get_duration(filename=p)
    except Exception:
        print(f'Librosa Parse Error: {p}, please check!')
    return t 

def split_BD(bp,whether_speakerID):
    audio_dict = {}
    # ap = os.path.join(bp,"AutomaticCompEval_Carbon")
    locale = os.path.basename(bp)
    res_f_n = f"Carbon_srdata_{locale}_speech-to-text.txt"
    res_f_p = ""
    for r,d,fs in os.walk(bp):
        for f in fs:
            if f.endswith(".wav"):
                audio_d = get_duration(os.path.join(r,f))
                audio_dict[f] = audio_d     #{'ar-AE-xveuRcJ2roM-7.wav': 321.0,...}
            if f == res_f_n:
                res_f_p = os.path.join(r,f)
    if not res_f_p:
        raise "no wer output error"
    WER_info_dict = {}
    with open(res_f_p,'r',encoding="utf-8") as fr:
        lines = fr.readlines()
    for line in lines[1:]:
        file_name = os.path.basename(line.split("\t")[1])
        wer = float(line.strip().split("\t")[-1])

        deletion = line.strip().split("\t")[-2]
        substitution =  line.strip().split("\t")[-3]
        insertion = line.strip().split("\t")[-4]
        wordcount = line.strip().split("\t")[-5]

        WER_info_dict[file_name] = [wordcount,insertion,substitution,deletion,wer]  #{'ar-AE-2QugwSPocGU-8.wav': ['176', '0', '11', '1', 6.82],...}

    begin_count = len(audio_dict) // 2
    total_dur = sum(audio_dict.values())
    target_dur = total_dur / 2
    loop_count = 1000
    is_split = False
    while begin_count:
        for i in range(loop_count):
            btest_l = random.sample(list(audio_dict.keys()),begin_count)  #random.sample:  不重复取样 begin_count 
            dtest_l = [x for x in list(audio_dict.keys()) if x not in btest_l ]
            btest_dur = sum([audio_dict[x] for x in btest_l])

            #WER公式计算
            btest_del = sum([int(WER_info_dict[x][3]) for x in btest_l])
            btest_sub = sum([int(WER_info_dict[x][2]) for x in btest_l])
            btest_ins = sum([int(WER_info_dict[x][1]) for x in btest_l])
            btest_word = sum([int(WER_info_dict[x][0]) for x in btest_l])
            b_WER_calculate = (btest_del + btest_ins + btest_sub)/btest_word*100

            dtest_del = sum([int(WER_info_dict[x][3]) for x in dtest_l])
            dtest_sub = sum([int(WER_info_dict[x][2]) for x in dtest_l])
            dtest_ins = sum([int(WER_info_dict[x][1]) for x in dtest_l])
            dtest_word = sum([int(WER_info_dict[x][0]) for x in dtest_l])
            d_WER_calculate = (dtest_del + dtest_ins + dtest_sub)/dtest_word*100



            #WER值平均
            btest_wer = sum([int(WER_info_dict[x][-1]) for x in btest_l])/ len(btest_l)
            dtest_wer = sum([int(WER_info_dict[x][-1]) for x in dtest_l])/ len(dtest_l)
            if abs(target_dur - btest_dur) < 300 and abs(btest_wer - dtest_wer) < 1.5:
                if abs(b_WER_calculate - d_WER_calculate) < 1.5:
                    print("split is gooooooooooooood!",'btest_wer: {} dtest_wer:{} b_WER_calculate:{} d_WER_calculate:{}'.format(btest_wer,dtest_wer,b_WER_calculate,d_WER_calculate))
                    is_split = True
                    break
        begin_count -= 1
        if is_split or begin_count < 10:
            break
    # verify res
    temp_set = set(btest_l) & set(dtest_l)
    if temp_set:
        raise "split error"
    test_list = ["BTEST","DTEST"]
    for t in test_list:
        if t == "BTEST":
            temp_list = btest_l
        else:
            temp_list = dtest_l
        t_p = os.path.join(bp,t)
        t_raw_p = os.path.join(bp,t+"_raw")
        ra_p = os.path.join(bp,'wav')       #也许之后会有文件名冲突
        rt_p = os.path.join(bp,'tsv')

        # copy audio
        for a in temp_list:
            ta_p = os.path.join(t_p,"Audio")
            ta_raw_p = os.path.join(t_raw_p,"wav")
            if not os.path.exists(ta_p):
                os.makedirs(ta_p)
            if not os.path.exists(ta_raw_p):
                os.makedirs(ta_raw_p)
            shutil.copy(os.path.join(ra_p,a),ta_p)
            shutil.copy(os.path.join(ra_p,a),ta_raw_p)

        # deal tsv
        res_list = []
        for a in temp_list:
            at = a.replace(".wav",".tsv")
            at_p = os.path.join(rt_p,at)
            tt_raw_p = os.path.join(t_raw_p,"tsv")
            if not os.path.exists(tt_raw_p):
                os.makedirs(tt_raw_p)
            shutil.copy(at_p,tt_raw_p)
            with open(at_p,'r',encoding="utf-8-sig") as fr:
                lines = fr.readlines()
            temp_trans = ""
            for s in lines:                 #对于文本文件内容不同有可能报错
                # print(at_p)
                f_p,s_p = s.split(']',1)
                s_time,e_time = f_p.replace('[', '').split(' ')
                if whether_speakerID == '1':
                    trans_info = s_p.strip().split(' ',1)[1]
                elif whether_speakerID == '0':
                    trans_info = s_p.strip()
                trans_info = '[{} {}] {}'.format(s_time,e_time,trans_info)
                temp_trans = temp_trans + trans_info + " "
            res_list.append(f"{a}\t{temp_trans}\n")
        with open(os.path.join(t_p,"transcription.tsv"),'w',encoding="utf-8") as fw:
            fw.write("".join(res_list))

    # get audio info
    b_test_a = os.path.join(bp,"BTEST")
    d_test_a = os.path.join(bp,"DTEST")
    final_res_list = []
    locale = os.path.basename(bp)
    b_res = chcek_audio_framerate_wave_new(b_test_a)
    d_res = chcek_audio_framerate_wave_new(d_test_a)
    final_res_list.append([locale,'btest',b_res["wav_count"],b_res["total_duration"],round(btest_wer),round(b_WER_calculate)])
    final_res_list.append([locale,'dtest',d_res["wav_count"],d_res["total_duration"],round(dtest_wer),round(d_WER_calculate)])
    ffp =  r"E:\v-yuhangxing\tool\divide_BD_test_set\all_divide_testset_infomation.csv"
    if not os.path.isfile(ffp) or os.path.getsize(ffp) == 0:
        with open(ffp,'a',encoding="utf-8") as fw:
            writer = csv.writer(fw)
            writer.writerows(['locale','testset','wav_count','total_durtation','WER','WER_calculate'])
    with open(ffp,'a',encoding="utf-8") as fw:
        writer = csv.writer(fw)
        writer.writerows(final_res_list)


# split_BD(r"D:\v-yuhangxing\data\FY23-IS-Meeting-Testset-Collection_TX\ar-AE\ar-AE")
split_BD(sys.argv[1],sys.argv[2])   #1--with speaker ID; 0--without speaker ID