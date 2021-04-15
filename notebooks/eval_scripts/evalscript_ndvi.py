evalscript_ndvi = """
//VERSION=3
    function setup() {
      return{
        input: [{ bands: ["B04", "B08"] }],
        output: { id: "default", bands: 1 }
      }
    }
    function evaluatePixel(sample) {
      let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04)
      return [ ndvi ]
    }

"""