static const UINT8 eei_back_normal_small_planedata_grey[64] = {
 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf,
 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf,
 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf,
 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf,
 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf, 0xff, 0xbf,
 0xff, 0xbf, 0xbf, 0xbf,
};
static EEI_IMAGE eei_back_normal_small = { 64, 64, NULL, {
    { eei_back_normal_small_planedata_grey, 64 },
    { eei_back_normal_small_planedata_grey, 64 },
    { eei_back_normal_small_planedata_grey, 64 },
    { NULL, 0 },
} };