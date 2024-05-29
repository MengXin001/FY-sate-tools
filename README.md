# FY-sate-tools
Simple Python toys for Fengyun & Gaofen satellites data processing

## FY3D-MWRI / FY3G-MWRI-RM
FY-3D/3G微波成像仪一级产品
### MWRI
```
FY3D_MWRIA_GBAL_L1_YYYYMMDD_HHmm_010KM_MS.HDF 升轨
FY3D_MWRID_GBAL_L1_YYYYMMDD_HHmm_010KM_MS.HDF 降轨
```
MWRI-RM 共 4 个馈源，其中，10.65GHz、36.5GHz 和 89GHz 为独立馈源，18.7GHz 及 23.8GHz 共用馈源。  

FY-3D 微波成像仪由于使用同一个主天线进行对地倾斜观测，因此地面足迹为大小不同的椭圆。

10.65GHz 地面足迹大小为 51Km×85Km，18.7GHz 地面足迹大小为 30Km×50Km，23.8GHz 地面足迹大小为 30Km×50Km，36.5GHz 地面足迹大小为 18Km×30Km，89GHz 地面足迹大小为 9Km×15Km。  

### MWRI-RM
```
FY3G_MWRI-_ORBA/D_L1_YYYYMMDD_HHmm_7000M_Vn.HDF
```
MWRI-RM 共 8 个馈源，分布在两排。  
第一排由通道 10GHz、18.7GHZ、23.8GHz、36GHz 以及 89GHz 构成，需要说明的是 18.7GHz 与 23.8GHz 共用一个馈源。  
第二排由通道 54GHz、118GHz、166GHz 以及 183GHz 构成。  

不同排的馈源由于观测几何存在角度上的差异，因此数据集也分为了S1与S2。MWRI-RM共17个频点，26 个通道（有些频点为双极化）。
## FY3G-PMR
FY-3G双频单极化Ku波段一维相控阵降水测量雷达二级产品
```
FY3G_PMR--_ORBA_L2_KuR_MLT_NUL_YYYYMMDD_HHmm_5000M_V0.HDF 升轨
FY3G_PMR--_ORBD_L2_KuR_MLT_NUL_YYYYMMDD_HHmm_5000M_V0.HDF 降轨
```
SLV反演数据集中使用的环境参数来自于ERA5再分析资料。

估计地表衰减订正后的雷达反射率因子（zFactorCorrectedESurface，float32，维数：nscan×nray）单位为dBZ，有效值范围0到70。

地理信息数据集为每个波束分别计算了地球椭球表面（第一维）和地球椭球之上约 18km 高度（第二维）两个位置的瞬时视场中心的地球经纬度。`level`默认使用第二维18km高度层地理信息。
```
io = PMRReader(fname, datafield="SLV", dataset="zFactorCorrectedESurface", level=0)
```