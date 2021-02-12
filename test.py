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
