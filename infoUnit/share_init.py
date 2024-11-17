import infoUnit.ShareUnit as ShareUnit

# 工商银行
GongShangYinHang = "601398.SH"

# 农商银行
NongShangYinHang = "601288.SH"


# 所有可用上证股票
valid_sh_share_list = [GongShangYinHang, NongShangYinHang]
valid_sh_share_dict = {
    share: ShareUnit.ShareUnit(share) for share in valid_sh_share_list
}
def get_valid_share(target="SH"):
    return valid_sh_share_dict