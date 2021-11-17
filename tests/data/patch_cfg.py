from . import lotr_text

lookup = {
    
    #--------------------
    # !lotr
    #--------------------
    "http://lotrproject.com/quotes/quote/64": {
        "text": lotr_text.text,
        "return": "there"
    },

    #--------------------
    # !cat
    #--------------------
    "https://next": {
        "another": "thing",
        "to": "return"
    },

    #--------------------
    # !pspop
    #--------------------
    "https://ps2.fisu.pw/api/population/?world=17": {
        "result": [
            {
                "vs": "99",
                "nc": "99",
                "tr": "99",
                "ns": "99"
            }
        ]
    },
    "https://ps2.fisu.pw/api/population/?world=1": {
        "result": [
            {
                "vs": "100",
                "nc": "100",
                "tr": "100",
                "ns": "100"
            }
        ]
    },
    "https://ps2.fisu.pw/api/population/?world=10": {
        "result": [
            {
                "vs": "101",
                "nc": "101",
                "tr": "101",
                "ns": "101"
            }
        ]
    }
}