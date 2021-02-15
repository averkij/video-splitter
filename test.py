#%%
import srt

# %%
with open('video\sub_rus2.srt', mode="r", encoding="utf-8") as input_file: 
    res = list(srt.parse("\n".join([x.rstrip() for x in input_file.readlines()])))
# %%
res[0]
# %%
srt.compose(res)
# %%
srt.timedelta_to_srt_timestamp(res[0].start)
# %%
import re 
res[0].content
# %%
s = "\nasd \tasd\nasd \t33 s\n\n asd"
s = re.sub(r"\r?\n|r", '', s).replace("\t",'')

print(s)
# %%
print(a)
# %%
