from infoUnit.ShareUnit import ShareUnit

gongHang = ShareUnit("601398.SH")
nongHang = ShareUnit("601288.SH")
# avg_ratio, cnt = gongHang.get_average_dividend_ratio()
# print(round(avg_ratio, 3))

# ratio_dict = nongHang.get_dividend_ratio()
# for k,v in ratio_dict.items():
#     print(k,v)

gongHang.show_mean()
# gongHang.show_mean(start_date="20150101")