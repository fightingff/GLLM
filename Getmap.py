import datetime
import matplotlib.pyplot as plt
from aenum import MultiValueEnum
from matplotlib.colors import BoundaryNorm, ListedColormap
from sentinelhub import CRS, BBox, DataCollection, SHConfig
from eolearn.core import EOWorkflow, FeatureType, LoadTask, OutputTask, SaveTask, linearly_connect_tasks
from eolearn.io import SentinelHubDemTask, SentinelHubEvalscriptTask, SentinelHubInputTask
import shutil

class SCL(MultiValueEnum):
    """Enum class containing basic LULC types"""

    NO_DATA = "no data", 0, "#000000"
    SATURATED_DEFECTIVE = "saturated / defective", 1, "#ff0004"
    DARK_AREA_PIXELS = "dark area pixels", 2, "#868686"
    CLOUD_SHADOWS = "cloud shadows", 3, "#774c0b"
    VEGETATION = "vegetation", 4, "#10d32d"
    BARE_SOILS = "bare soils", 5, "#ffff53"
    WATER = "water", 6, "#0000ff"
    CLOUDS_LOW_PROBA = "clouds low proba.", 7, "#818181"
    CLOUDS_MEDIUM_PROBA = "clouds medium proba.", 8, "#c0c0c0"
    CLOUDS_HIGH_PROBA = "clouds high proba.", 9, "#f2f2f2"
    CIRRUS = "cirrus", 10, "#bbc5ec"
    SNOW_ICE = "snow / ice", 11, "#53fffa",

    @property
    def rgb(self):
        return [c / 255.0 for c in self.rgb_int]

    @property
    def rgb_int(self):
        hex_val = self.values[2][1:]
        return [int(hex_val[i : i + 2], 16) for i in (0, 2, 4)]


scl_bounds = [-0.5 + i for i in range(len(SCL) + 1)]
scl_cmap = ListedColormap([x.rgb for x in SCL], name="scl_cmap")
scl_norm = BoundaryNorm(scl_bounds, scl_cmap.N)

def GetImage(latitude, longitude,  time="", path="*.png"):
    try:
        shutil.rmtree("io_example")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    CLIENT_ID = "961a15b7-2700-4d76-bb45-16b8d3a0e0db"
    CLIENT_SECRET = "OZDYnvKISvTwzZlR46SzzBbcZlgqx6wp"

    config = SHConfig()

    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET
    config.instance_id="cf23a0df-da1a-49ee-8706-922ca9d48f04"
    if config.sh_client_id == "" or config.sh_client_secret == "" or config.instance_id == "":
        print("Warning! To use Sentinel Hub services, please provide the credentials (client ID and client secret).")

    # position of the map
    roi_bbox = BBox(bbox=[longitude - 0.05, latitude - 0.05, longitude + 0.05, latitude + 0.05], crs=CRS.WGS84)

    # time interval of downloaded data
    time_interval = ("2020-04-01", "2020-05-01")

    # maximal cloud coverage (based on Sentinel-2 provided tile metadata)
    maxcc = 0.8

    # resolution of the request (in metres)
    resolution = 10

    # time difference parameter (minimum allowed time difference; if two observations are closer than this,
    # they will be mosaicked into one observation)
    time_difference = datetime.timedelta(hours=2)

    # input_task = SentinelHubInputTask(
    #     data_collection=DataCollection.SENTINEL2_L1C,
    #     bands=["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B10", "B11", "B12"],
    #     bands_feature=(FeatureType.DATA, "L1C_data"),
    #     additional_data=[(FeatureType.MASK, "dataMask")],
    #     resolution=resolution,
    #     maxcc=maxcc,
    #     time_difference=time_difference,
    #     config=config,
    #     max_threads=3,
    # )

    # indices_evalscript = """
    #     //VERSION=3

    #     function setup() {
    #         return {
    #             input: ["B03","B04","B08","dataMask"],
    #             output:[{
    #                 id: "indices",
    #                 bands: 2,
    #                 sampleType: SampleType.FLOAT32
    #             }]
    #         }
    #     }

    #     function evaluatePixel(sample) {
    #         let ndvi = index(sample.B08, sample.B04);
    #         let ndwi = index(sample.B03, sample.B08);
    #         return {
    #         indices: [ndvi, ndwi]
    #         };
    #     }
    # """

    # this will add two indices: ndvi and ndwi
    # add_indices = SentinelHubEvalscriptTask(
    #     features=[(FeatureType.DATA, "indices")],
    #     evalscript=indices_evalscript,
    #     data_collection=DataCollection.SENTINEL2_L1C,
    #     resolution=resolution,
    #     maxcc=maxcc,
    #     time_difference=time_difference,
    #     config=config,
    #     max_threads=3,
    # )

    add_dem = SentinelHubDemTask(
        feature="dem", data_collection=DataCollection.DEM_COPERNICUS_30, resolution=resolution, config=config
    )

    add_l2a_and_scl = SentinelHubInputTask(
        data_collection=DataCollection.SENTINEL2_L2A,
        bands=["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"],
        bands_feature=(FeatureType.DATA, "L2A_data"),
        additional_data=[(FeatureType.MASK, "SCL")],
        resolution=resolution,
        maxcc=maxcc,
        time_difference=time_difference,
        config=config,
        max_threads=3,
    )

    save = SaveTask("io_example")
    output_task = OutputTask("eopatch")

    # workflow_nodes = linearly_connect_tasks(input_task, add_indices, add_l2a_and_scl, add_dem, save, output_task)
    workflow_nodes = linearly_connect_tasks(add_l2a_and_scl, add_dem, save, output_task)
    workflow = EOWorkflow(workflow_nodes)

    result = workflow.execute(
        {
            workflow_nodes[0]: {"bbox": roi_bbox, "time_interval": time_interval},
            workflow_nodes[-2]: {"eopatch_folder": "eopatch"},
        }
    )

    eopatch = result.outputs["eopatch"]
    print(eopatch)


    # plot and save the RGB image
    plt.figure(figsize=(10, 10))
    plt.imshow(eopatch.mask["SCL"][0].squeeze(),cmap=scl_cmap, norm=scl_norm)
    plt.axis("off")
    plt.savefig(path)
