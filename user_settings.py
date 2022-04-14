# 写入你的服务器编号，下面是示例
LOCAL_SERVER = ['ShenQuanHen']

CN_MOGULI = ['BaiYinXiang', 'BaiJinHuanXiang', 'ShenQuanHen', 'ChaoFengTing', 'LvRenZhanQiao',
                  'FuXiaoZhiJian', 'LongChaoShenDian', 'MengYuBaoJing']

# 北美服务器 NA servers
NA_AETHER = ['Adamantoise', 'Cactuar', 'Faerie', 'Gilgamesh', 'Jenova', 'Midgardsormr', 'Sargatanas', 'Siren']
NA_PRIMAL = ['Behemoth', 'Excalibur', 'Exodus', 'Famfrit', 'Hyperion', 'Lamia', 'Leviathan', 'Ultros']
NA_CRYSTAL = ['Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro' , 'Mateus', 'Zalera']


TARGET_ITEMS = ['34691', '34541', '34391', '34241', '34091',
                '33942', '33932', '35463']

SERVERS_COLLECTION = [CN_MOGULI, NA_AETHER, NA_PRIMAL, NA_CRYSTAL]

TARGET_SERVERS = []
for server in LOCAL_SERVER:
    for i in SERVERS_COLLECTION:
        if server in i:
            TARGET_SERVERS.append(i)


