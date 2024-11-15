import infoUnit.ShareUnit as ShareUnit

# 工商银行
GongShangYinHang = "601398.SH"

# 农商银行
NongShangYinHang = "601288.SH"

def get_valid_share():
    valid_share_list = [GongShangYinHang, NongShangYinHang]
    valid_share_dict = {
        share: ShareUnit.ShareUnit(share) for share in valid_share_list
    }
    return valid_share_dict