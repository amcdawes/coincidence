import streamlit as st
from coincCounter import CoincidenceCounter
from countPlotter import countFig

cc = CoincidenceCounter()
cc.update_data()

st.metric("AB", cc.ab[-1])
st.metric("AB'", cc.abp[-1])

#todo move counter data to pandas dataframe!
fig, ax = countFig()

ax.clear() # this clears too much, gridlines and labels, tried del ax.lines but warning
ax.bar(x=cc.singleLabels, height=cc.singles, color="red")
ax.set_ylim(0,350000)
st.pyplot(fig)

st.experimental_rerun()