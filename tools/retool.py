#正则表达式工具
import re

#精确的匹配给定的字符串是否是IP地址
def matchipv4(line):
    return re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", str(line))


#todo 完成下列代码整理

# #简单的从长文本中提取中提取ip地址
# string_ip = "is this 289.22.22.22 ip ?"
# result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", string_ip)
# if result:
#     print result
# else:
#     print "re cannot find ip"
# #精确提取IP
# result = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", string_ip):
# if result:
#     print result
# else:
#     print "re cannot find ip"
#
#     string_IPv6 = "1050:0:0:0:5:600:300c:326b"
#     # 匹配是否满足IPv6格式要求,请注意例子里大小写不敏感
#     if re.match(r"^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$", string_IPv6, re.I):
#         print
#         "IPv6 vaild"
#     else:
#         print
#         "IPv6 invaild"
#     # 提取IPv6，例子里大小写不敏感
#     result = re.findall(r"(?<![:.\w])(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}(?![:.\w])", string_IPv6, re.I)
#     # 打印提取结果
#     print
#     result