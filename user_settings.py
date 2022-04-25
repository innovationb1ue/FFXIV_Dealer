# Configure your own setting in below lines
# 写入你的服务器编号，下面是示例
# Write your own server name below
LOCAL_SERVER = ['ShenQuanHen']
# 想要倒卖的物品号, 可由universalis.app的物品页面获得
# for example https://universalis.app/market/34535 means the item id is 34535
TARGET_ITEMS = ['34691', '34541', '34391', '34241', '34091',
                '33942', '33932', '35463']


# Other macros below (**NO** Need To Modify)
CN_MOGULI = ['BaiYinXiang', 'BaiJinHuanXiang', 'ShenQuanHen', 'ChaoFengTing', 'LvRenZhanQiao',
                  'FuXiaoZhiJian', 'LongChaoShenDian', 'MengYuBaoJing']
CN_LUXINGNIAO = ['HongYuHai', 'YanXia', 'JingYuZhuangYuan']
# 北美服务器 NA servers
NA_AETHER = ['Adamantoise', 'Cactuar', 'Faerie', 'Gilgamesh', 'Jenova', 'Midgardsormr', 'Sargatanas', 'Siren']
NA_PRIMAL = ['Behemoth', 'Excalibur', 'Exodus', 'Famfrit', 'Hyperion', 'Lamia', 'Leviathan', 'Ultros']
NA_CRYSTAL = ['Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro' , 'Mateus', 'Zalera']

SERVERS_COLLECTION = [CN_MOGULI, CN_LUXINGNIAO, NA_AETHER, NA_PRIMAL, NA_CRYSTAL]

TARGET_SERVERS = []
for server in LOCAL_SERVER:
    for i in SERVERS_COLLECTION:
        if server in i:
            TARGET_SERVERS.append(i)


