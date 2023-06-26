

vanilla_headers = {
	0x0000: [0x41, 0x21, 0x13, 0x22, 0x07, 0x3D, 0x00, 0x00, 0x00, 0x10, 0xC0, 0x00, 0x00, 0x04],
	0x0001: [0xC0, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x72, 0x00, 0x50, 0x52],
	0x0002: [0xC0, 0x1D, 0x04, 0x06, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00, 0x18, 0x0D],
	0x0003: [0xC0, 0x07, 0x06, 0x19, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x02, 0x12, 0x00, 0x00, 0x00],
	0x0004: [0x00, 0x18, 0x0D, 0x26, 0x00, 0x26, 0x14, 0x00, 0x00, 0x00, 0xB5, 0x00, 0x08, 0x08],
	0x0005: [0x00, 0x08, 0x08, 0x14, 0x00, 0x25, 0x00, 0x20, 0x06, 0x05, 0x0C, 0x00, 0x25, 0x00],
	0x0006: [0x00, 0x08, 0x08, 0x14, 0x00, 0x25, 0x00, 0x20, 0x06, 0x05, 0x0C, 0x00, 0x25, 0x00],
	0x0007: [0x20, 0x06, 0x05, 0x0C, 0x00, 0x25, 0x00, 0x00, 0x00, 0x17, 0x17, 0xC0, 0x07, 0x06],
	0x0008: [0xC0, 0x07, 0x06, 0x07, 0x00, 0x00, 0x00, 0x00, 0x0F, 0x07, 0x19, 0x00, 0x27, 0x00],
	0x0009: [0x00, 0x0F, 0x07, 0x19, 0x00, 0x27, 0x00, 0x00, 0x00, 0x4B, 0x4A, 0x4A, 0x00, 0x0F],
	0x000A: [0x00, 0x0F, 0x07, 0x19, 0x00, 0x27, 0x00, 0x00, 0x00, 0x09, 0x3A, 0x01, 0x0F, 0x07],
	0x000B: [0x01, 0x0F, 0x07, 0x19, 0x00, 0x03, 0x00, 0x00, 0x00, 0x6A, 0x1B, 0xC0, 0x28, 0x0E],
	0x000C: [0xC0, 0x28, 0x0E, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6B, 0x8C, 0x8C, 0x40],
	0x000D: [0x40, 0x1B, 0x0E, 0x18, 0x05, 0x38, 0x00, 0x00, 0x13, 0x0B, 0x1C, 0x00, 0x08, 0x00],
	0x000E: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x1E, 0x00, 0x21, 0x13],
	0x000F: [0x00, 0x21, 0x13, 0x22, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00],
	0x0010: [0x00, 0x21, 0x13, 0x22, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00],
	0x0011: [0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x02, 0xC0, 0x1D, 0x04],
	0x0012: [0xC0, 0x1D, 0x04, 0x06, 0x00, 0x00, 0x00, 0x00, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00],
	0x0013: [0x00, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00, 0x00, 0x18, 0x0D, 0x1E, 0x00, 0x00, 0x00],
	0x0014: [0x20, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00, 0xC0, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00],
	0x0015: [0xC0, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB6, 0x90, 0x08, 0x08],
	0x0016: [0x90, 0x08, 0x08, 0x11, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x66, 0x20, 0x06, 0x05],
	0x0017: [0x20, 0x06, 0x05, 0x19, 0x00, 0x35, 0x00, 0x00, 0x00, 0x27, 0x07, 0x27, 0x01, 0x0F],
	0x0018: [0x00, 0x07, 0x06, 0x07, 0x00, 0x00, 0x00, 0x00, 0x22, 0x12, 0x07, 0x00, 0x00, 0x00],
	0x0019: [0x01, 0x0F, 0x07, 0x19, 0x00, 0x00, 0x00, 0x00, 0x0F, 0x07, 0x19, 0x00, 0x16, 0x00],
	0x001A: [0x00, 0x0F, 0x07, 0x19, 0x00, 0x16, 0x00, 0x00, 0x00, 0x00, 0x6A, 0x6A, 0x68, 0x0F],
	0x001B: [0x68, 0x0F, 0x07, 0x08, 0x00, 0x03, 0x1C, 0x00, 0x00, 0x00, 0x0B, 0x00, 0x1A, 0x0E],
	0x001C: [0x00, 0x1A, 0x0E, 0x09, 0x00, 0x04, 0x3F, 0x00, 0x00, 0x00, 0x8C, 0x00, 0x1B, 0x0E],
	0x001D: [0x00, 0x1B, 0x0E, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4C, 0x20, 0x13, 0x0B],
	0x001E: [0x20, 0x13, 0x0B, 0x1C, 0x00, 0x17, 0x00, 0x00, 0x00, 0x3E, 0x0E, 0x00, 0x13, 0x0B],
	0x001F: [0x00, 0x13, 0x0B, 0x29, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x3F, 0x20, 0x0C, 0x02],
	0x0020: [0x20, 0x0C, 0x02, 0x12, 0x00, 0x15, 0x25, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00],
	0x0021: [0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x18, 0x0D, 0x26, 0x00, 0x01, 0x00],
	0x0022: [0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x18, 0x0D, 0x26, 0x00, 0x01, 0x00],
	0x0023: [0x00, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00, 0x00, 0x18, 0x0D, 0x1E, 0x00, 0x00, 0x00],
	0x0024: [0x00, 0x18, 0x0D, 0x26, 0x00, 0x01, 0x00, 0x00, 0x0A, 0x08, 0x11, 0x00, 0x16, 0x00],
	0x0025: [0x00, 0x0A, 0x08, 0x11, 0x00, 0x16, 0x00, 0x00, 0x00, 0x00, 0x76, 0x76, 0x76, 0x20],
	0x0026: [0x00, 0x0A, 0x08, 0x11, 0x00, 0x16, 0x00, 0x00, 0x00, 0x00, 0x76, 0x76, 0x76, 0x20],
	0x0027: [0x20, 0x06, 0x05, 0x19, 0x00, 0x36, 0x00, 0x00, 0x00, 0x31, 0x17, 0x31, 0x80, 0x0A],
	0x0028: [0x80, 0x0A, 0x08, 0x11, 0x00, 0x32, 0x1B, 0x00, 0x00, 0x00, 0x38, 0xCC, 0x0E, 0x09],
	0x0029: [0xCC, 0x0E, 0x09, 0x1A, 0x02, 0x25, 0x00, 0x00, 0x0F, 0x07, 0x19, 0x00, 0x00, 0x00],
	0x002A: [0x00, 0x0F, 0x07, 0x19, 0x00, 0x00, 0x00, 0xC0, 0x0F, 0x07, 0x2B, 0x00, 0x16, 0x00],
	0x002B: [0xC0, 0x0F, 0x07, 0x2B, 0x00, 0x16, 0x00, 0x00, 0x00, 0x00, 0x3B, 0x00, 0x13, 0x0B],
	0x002C: [0x00, 0x07, 0x06, 0x07, 0x00, 0x00, 0x00, 0x00, 0x22, 0x12, 0x07, 0x00, 0x00, 0x00],
	0x002D: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x2A, 0x00, 0xC0, 0x07, 0x06, 0x19, 0x00, 0x00, 0x00],
	0x002E: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x2A, 0x00, 0xC0, 0x07, 0x06, 0x19, 0x00, 0x00, 0x00],
	0x002F: [0xC0, 0x07, 0x06, 0x19, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x02, 0x12, 0x00, 0x00, 0x00],
	0x0030: [0x00, 0x0C, 0x02, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x20, 0x06, 0x05],
	0x0031: [0x20, 0x06, 0x05, 0x19, 0x00, 0x37, 0x04, 0x22, 0x00, 0x77, 0x27, 0x77, 0x01, 0x01],
	0x0032: [0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x42, 0x00, 0x04, 0x05],
	0x0033: [0x00, 0x04, 0x05, 0x0B, 0x00, 0x15, 0x25, 0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00],
	0x0034: [0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x54, 0x80, 0x0A, 0x08],
	0x0035: [0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x19, 0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00],
	0x0036: [0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00, 0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00],
	0x0037: [0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x19, 0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00],
	0x0038: [0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x28, 0x20, 0x0D, 0x09],
	0x0039: [0x20, 0x0D, 0x09, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x29, 0x20, 0x0F, 0x07, 0x19],
	0x003A: [0x20, 0x0F, 0x07, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x0A, 0x00, 0x0F, 0x07],
	0x003B: [0x00, 0x0F, 0x07, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2B, 0x00, 0x07, 0x06],
	0x003C: [0x00, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00, 0x20, 0x1A, 0x0E, 0x0C, 0x00, 0x33, 0x00],
	0x003D: [0x20, 0x1A, 0x0E, 0x0C, 0x00, 0x33, 0x00, 0x00, 0x00, 0x96, 0x96, 0xCC, 0x13, 0x0B],
	0x003E: [0xCC, 0x13, 0x0B, 0x29, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x1E, 0x00, 0x13, 0x0B],
	0x003F: [0x00, 0x13, 0x0B, 0x29, 0x00, 0x27, 0x14, 0x00, 0x00, 0x00, 0x1F, 0x5F, 0xC0, 0x00],
	0x0040: [0xC0, 0x00, 0x02, 0x27, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0xB0, 0x01, 0x00],
	0x0041: [0x01, 0x00, 0x00, 0x02, 0x00, 0x13, 0x00, 0x00, 0x00, 0x00, 0x42, 0x01, 0x01, 0x01],
	0x0042: [0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x41, 0x32, 0x68, 0x04],
	0x0043: [0x68, 0x04, 0x05, 0x0A, 0x00, 0x00, 0x1D, 0x00, 0x17, 0x0A, 0x1B, 0x00, 0x01, 0x00],
	0x0044: [0x00, 0x17, 0x0A, 0x1B, 0x00, 0x01, 0x00, 0x60, 0x17, 0x0A, 0x1B, 0x00, 0x01, 0x00],
	0x0045: [0x60, 0x17, 0x0A, 0x1B, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0xBC, 0x00, 0x0A, 0x08],
	0x0046: [0x00, 0x0A, 0x08, 0x11, 0x00, 0x3C, 0x00, 0x00, 0x0D, 0x09, 0x13, 0x00, 0x33, 0x34],
	0x0047: [0x00, 0x0D, 0x09, 0x13, 0x00, 0x33, 0x34, 0x00, 0x0F, 0x07, 0x19, 0x00, 0x17, 0x00],
	0x0048: [0x00, 0x0D, 0x09, 0x13, 0x00, 0x33, 0x34, 0x00, 0x0F, 0x07, 0x19, 0x00, 0x17, 0x00],
	0x0049: [0x00, 0x0D, 0x09, 0x13, 0x00, 0x33, 0x34, 0x00, 0x0F, 0x07, 0x19, 0x00, 0x17, 0x00],
	0x004A: [0x00, 0x0F, 0x07, 0x19, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x09, 0x09, 0x00, 0x0F],
	0x004B: [0x00, 0x0F, 0x07, 0x08, 0x00, 0x01, 0x00, 0x00, 0x00, 0x09, 0x00, 0x1A, 0x0E, 0x0C],
	0x004C: [0x00, 0x1A, 0x0E, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1D, 0x20, 0x1A, 0x0E],
	0x004D: [0x20, 0x1A, 0x0E, 0x0C, 0x00, 0x32, 0x3F, 0x00, 0x00, 0xA6, 0xA6, 0x00, 0x13, 0x0B],
	0x004E: [0x00, 0x13, 0x0B, 0x29, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x13, 0x0B],
	0x004F: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0xBE, 0xC0, 0x00, 0x00, 0x04],
	0x0050: [0xC0, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01],
	0x0051: [0xC0, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x61, 0xC0, 0x00, 0x00],
	0x0052: [0xC0, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01],
	0x0053: [0xC0, 0x04, 0x05, 0x0A, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x63, 0x20, 0x0A, 0x08],
	0x0054: [0x20, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x34, 0x34, 0x01, 0x01, 0x10],
	0x0055: [0x01, 0x01, 0x10, 0x0D, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x09, 0x13, 0x00, 0x23, 0x00],
	0x0056: [0x00, 0x0D, 0x09, 0x13, 0x00, 0x23, 0x00, 0x00, 0x0D, 0x09, 0x13, 0x00, 0x16, 0x00],
	0x0057: [0x00, 0x0D, 0x09, 0x13, 0x00, 0x16, 0x00, 0x00, 0x0D, 0x09, 0x13, 0x00, 0x21, 0x28],
	0x0058: [0x00, 0x0D, 0x09, 0x13, 0x00, 0x21, 0x28, 0xC0, 0x0D, 0x09, 0x13, 0x00, 0x00, 0x00],
	0x0059: [0xC0, 0x0D, 0x09, 0x13, 0x00, 0x00, 0x00, 0x00, 0x10, 0x07, 0x15, 0x00, 0x25, 0x00],
	0x005A: [0x00, 0x10, 0x07, 0x15, 0x00, 0x25, 0x00, 0xC0, 0x1B, 0x0E, 0x0A, 0x00, 0x17, 0x00],
	0x005B: [0xC0, 0x1B, 0x0E, 0x0A, 0x00, 0x17, 0x00, 0x00, 0x1B, 0x0E, 0x0A, 0x00, 0x00, 0x00],
	0x005C: [0x00, 0x1B, 0x0E, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5D, 0x00, 0x24, 0x0E],
	0x005D: [0x00, 0x24, 0x0E, 0x23, 0x00, 0x09, 0x00, 0x00, 0x00, 0x00, 0x5C, 0x20, 0x13, 0x0B],
	0x005E: [0x20, 0x13, 0x0B, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7E, 0x7E, 0x00, 0x13, 0x0B],
	0x005F: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x27, 0x00, 0x00, 0x00, 0x00, 0x3F, 0x7F, 0xC0, 0x00],
	0x0060: [0xC0, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00],
	0x0061: [0xC0, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x51, 0x00, 0x09, 0x05],
	0x0062: [0xC0, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00],
	0x0063: [0x00, 0x09, 0x05, 0x0A, 0x00, 0x0D, 0x00, 0x00, 0x00, 0x00, 0x53, 0xE0, 0x23, 0x0A],
	0x0064: [0xE0, 0x23, 0x0A, 0x21, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0xAB, 0xE0, 0x23, 0x0A],
	0x0065: [0xE0, 0x23, 0x0A, 0x21, 0x00, 0x00, 0x00, 0x00, 0x00, 0xAC, 0xC0, 0x0A, 0x08, 0x11],
	0x0066: [0xC0, 0x0A, 0x08, 0x11, 0x00, 0x3C, 0x00, 0x00, 0x00, 0x00, 0x16, 0x00, 0x0D, 0x09],
	0x0067: [0x00, 0x0D, 0x09, 0x13, 0x00, 0x22, 0x00, 0x00, 0x0D, 0x09, 0x13, 0x00, 0x00, 0x00],
	0x0068: [0x00, 0x0D, 0x09, 0x13, 0x00, 0x00, 0x00, 0x01, 0x0F, 0x07, 0x19, 0x00, 0x00, 0x00],
	0x0069: [0x01, 0x0F, 0x07, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1A, 0x1A, 0x00, 0x1B],
	0x006A: [0x01, 0x0F, 0x07, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1A, 0x1A, 0x00, 0x1B],
	0x006B: [0x00, 0x1B, 0x0E, 0x0A, 0x00, 0x08, 0x0B, 0x00, 0x00, 0x00, 0x0C, 0x00, 0x24, 0x0E],
	0x006C: [0x00, 0x24, 0x0E, 0x23, 0x00, 0x03, 0x3F, 0x00, 0x00, 0x00, 0xA5, 0x00, 0x24, 0x0E],
	0x006D: [0x00, 0x24, 0x0E, 0x23, 0x00, 0x05, 0x00, 0x00, 0x13, 0x0B, 0x1C, 0x00, 0x02, 0x00],
	0x006E: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x4E, 0x00, 0x01, 0x01],
	0x006F: [0x00, 0x01, 0x01, 0x04, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x71, 0x80, 0xC0, 0x01],
	0x0070: [0x00, 0x01, 0x01, 0x04, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x71, 0x80, 0xC0, 0x01],
	0x0071: [0xC0, 0x01, 0x01, 0x04, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x70, 0xC0, 0x01, 0x01],
	0x0072: [0xC0, 0x01, 0x01, 0x04, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x01, 0x00, 0x09, 0x05],
	0x0073: [0x00, 0x09, 0x05, 0x0A, 0x00, 0x17, 0x00, 0x00, 0x09, 0x05, 0x0A, 0x00, 0x27, 0x00],
	0x0074: [0x00, 0x09, 0x05, 0x0A, 0x00, 0x27, 0x00, 0x00, 0x09, 0x05, 0x0A, 0x00, 0x01, 0x00],
	0x0075: [0x00, 0x09, 0x05, 0x0A, 0x00, 0x01, 0x00, 0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x18],
	0x0076: [0x80, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x26, 0x26, 0x26, 0xC0],
	0x0077: [0xC0, 0x06, 0x05, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA7, 0x31, 0x87, 0x87, 0x00],
	0x0078: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x03, 0x39, 0x00, 0x00, 0x9D, 0x00, 0x28, 0x0E, 0x13],
	0x0079: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x03, 0x39, 0x00, 0x00, 0x9D, 0x00, 0x28, 0x0E, 0x13],
	0x007A: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x03, 0x39, 0x00, 0x00, 0x9D, 0x00, 0x28, 0x0E, 0x13],
	0x007B: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x03, 0x39, 0x00, 0x00, 0x9D, 0x00, 0x28, 0x0E, 0x13],
	0x007C: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x20, 0x00, 0x00, 0x28, 0x0E, 0x13, 0x00, 0x04, 0x3C],
	0x007D: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x04, 0x3C, 0x00, 0x00, 0x9B, 0x20, 0x13, 0x0B, 0x1C],
	0x007E: [0x20, 0x13, 0x0B, 0x1C, 0x00, 0x2B, 0x17, 0x00, 0x00, 0x9E, 0x5E, 0x00, 0x13, 0x0B],
	0x007F: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5F, 0x60, 0x01, 0x01],
	0x0080: [0x60, 0x01, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0xC0, 0x01, 0x01],
	0x0081: [0xC0, 0x01, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x09, 0x05, 0x0A, 0x00, 0x0D, 0x00],
	0x0082: [0xC0, 0x01, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x09, 0x05, 0x0A, 0x00, 0x0D, 0x00],
	0x0083: [0x00, 0x09, 0x05, 0x0A, 0x00, 0x0D, 0x00, 0x00, 0x09, 0x05, 0x0A, 0x00, 0x00, 0x00],
	0x0084: [0x00, 0x09, 0x05, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x09, 0x05, 0x0A, 0x00, 0x02, 0x00],
	0x0085: [0x00, 0x09, 0x05, 0x0A, 0x00, 0x02, 0x00, 0x00, 0x06, 0x05, 0x19, 0x00, 0x3E, 0x01],
	0x0086: [0x00, 0x06, 0x05, 0x19, 0x00, 0x3E, 0x01, 0x28, 0x00, 0x00, 0x77, 0x77, 0x00, 0x0B],
	0x0087: [0x00, 0x06, 0x05, 0x19, 0x00, 0x3E, 0x01, 0x28, 0x00, 0x00, 0x77, 0x77, 0x00, 0x0B],
	0x0088: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x00, 0x00, 0x02, 0x00, 0xA9, 0x00, 0x28, 0x0E, 0x13],
	0x0089: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x00, 0x00, 0x02, 0x00, 0xA9, 0x00, 0x28, 0x0E, 0x13],
	0x008A: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x3A, 0x0C, 0x20, 0x28, 0x0E, 0x13, 0x00, 0x16, 0x00],
	0x008B: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x3A, 0x0C, 0x20, 0x28, 0x0E, 0x13, 0x00, 0x16, 0x00],
	0x008C: [0x20, 0x28, 0x0E, 0x13, 0x00, 0x16, 0x00, 0x28, 0x00, 0x1C, 0x0C, 0x0C, 0x1C, 0x00],
	0x008D: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x33, 0x29, 0x00, 0x13, 0x0B, 0x1C, 0x00, 0x00, 0x00],
	0x008E: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xAE, 0x80, 0x12, 0x0C],
	0x008F: [0x80, 0x12, 0x0C, 0x16, 0x00, 0x25, 0x00, 0x00, 0x11, 0x0C, 0x1C, 0x00, 0x00, 0x00],
	0x0090: [0x80, 0x12, 0x0C, 0x16, 0x00, 0x25, 0x00, 0x00, 0x11, 0x0C, 0x1C, 0x00, 0x00, 0x00],
	0x0091: [0x00, 0x11, 0x0C, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA0, 0x01, 0x11, 0x0C],
	0x0092: [0x01, 0x11, 0x0C, 0x1C, 0x00, 0x00, 0x00, 0x01, 0x11, 0x0C, 0x1C, 0x00, 0x16, 0x00],
	0x0093: [0x01, 0x11, 0x0C, 0x1C, 0x00, 0x16, 0x00, 0x08, 0x00, 0x00, 0xA2, 0x00, 0x25, 0x0E],
	0x0094: [0x00, 0x25, 0x0E, 0x24, 0x00, 0x00, 0x00, 0x00, 0x25, 0x0E, 0x24, 0x00, 0x33, 0x00],
	0x0095: [0x00, 0x25, 0x0E, 0x24, 0x00, 0x00, 0x00, 0x00, 0x25, 0x0E, 0x24, 0x00, 0x33, 0x00],
	0x0096: [0x00, 0x25, 0x0E, 0x24, 0x00, 0x33, 0x00, 0x00, 0x00, 0x00, 0x3D, 0x68, 0x11, 0x0C],
	0x0097: [0x68, 0x11, 0x0C, 0x1D, 0x00, 0x1C, 0x00, 0x00, 0x00, 0xD1, 0xD1, 0x00, 0x11, 0x0C],
	0x0098: [0x00, 0x11, 0x0C, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xD2, 0x01, 0x0B, 0x05],
	0x0099: [0x01, 0x0B, 0x05, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xDA, 0x00, 0x28, 0x0E],
	0x009A: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7D, 0x00, 0x28, 0x0E, 0x13],
	0x009B: [0x00, 0x28, 0x0E, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7D, 0x00, 0x28, 0x0E, 0x13],
	0x009C: [0x00, 0x28, 0x0E, 0x13, 0x06, 0x00, 0x00, 0x00, 0x28, 0x0E, 0x13, 0x06, 0x00, 0x3B],
	0x009D: [0x00, 0x28, 0x0E, 0x13, 0x06, 0x00, 0x3B, 0x00, 0x00, 0x7B, 0x20, 0x13, 0x0B, 0x1C],
	0x009E: [0x20, 0x13, 0x0B, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0xBE, 0xBE, 0x00, 0x13, 0x0B],
	0x009F: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x17, 0x00, 0x00, 0x12, 0x0C, 0x1D, 0x00, 0x00, 0x00],
	0x00A0: [0x00, 0x12, 0x0C, 0x1D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x91, 0x00, 0x11, 0x0C],
	0x00A1: [0x00, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00, 0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00],
	0x00A2: [0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x93, 0x60, 0x19, 0x0D],
	0x00A3: [0x00, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00, 0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00],
	0x00A4: [0x60, 0x19, 0x0D, 0x17, 0x04, 0x25, 0x00, 0x00, 0x25, 0x0E, 0x24, 0x00, 0x07, 0x00],
	0x00A5: [0x00, 0x25, 0x0E, 0x24, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x6C, 0x00, 0x25, 0x0E],
	0x00A6: [0x00, 0x25, 0x0E, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4D, 0x00, 0x06, 0x05],
	0x00A7: [0x00, 0x06, 0x05, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x17, 0xC0, 0x0B, 0x05, 0x08],
	0x00A8: [0xC0, 0x0B, 0x05, 0x08, 0x00, 0x03, 0x00, 0xC0, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00],
	0x00A9: [0xC0, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00, 0x00, 0x00, 0x89, 0xC0, 0x0B, 0x05, 0x08],
	0x00AA: [0xC0, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00, 0x00, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00],
	0x00AB: [0x00, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0xE0, 0x17, 0x0A],
	0x00AC: [0xE0, 0x17, 0x0A, 0x20, 0x00, 0x25, 0x00, 0x00, 0x13, 0x0B, 0x1C, 0x00, 0x27, 0x00],
	0x00AD: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x27, 0x00, 0x00, 0x00, 0x00, 0x8E, 0x00, 0x13, 0x0B],
	0x00AE: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x27, 0x00, 0x00, 0x00, 0x00, 0x8E, 0x00, 0x13, 0x0B],
	0x00AF: [0x00, 0x13, 0x0B, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x26, 0x02, 0x21, 0x00, 0x05, 0x02],
	0x00B0: [0x00, 0x26, 0x02, 0x21, 0x00, 0x05, 0x02, 0x08, 0x00, 0x00, 0x40, 0xC0, 0x00, 0x11],
	0x00B1: [0x00, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00, 0x02, 0x00, 0xB2, 0xC0, 0x11, 0x0C, 0x1D],
	0x00B2: [0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x03, 0x0E, 0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x27, 0x00],
	0x00B3: [0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x27, 0x00, 0x00, 0x19, 0x0D, 0x17, 0x00, 0x00, 0x00],
	0x00B4: [0x00, 0x19, 0x0D, 0x17, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC4, 0x01, 0x18, 0x0D],
	0x00B5: [0x01, 0x18, 0x0D, 0x25, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x18, 0x0D],
	0x00B6: [0x00, 0x18, 0x0D, 0x1E, 0x00, 0x04, 0x3C, 0x00, 0x00, 0x00, 0x15, 0x00, 0x0B, 0x05],
	0x00B7: [0x00, 0x18, 0x0D, 0x1E, 0x00, 0x00, 0x00, 0x20, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00],
	0x00B8: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x27, 0x00, 0xC0, 0x0B, 0x05, 0x08, 0x00, 0x00, 0x00],
	0x00B9: [0xC0, 0x0B, 0x05, 0x08, 0x00, 0x00, 0x00, 0x01, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00],
	0x00BA: [0x01, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00, 0x40, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00],
	0x00BB: [0x40, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x17, 0x0A, 0x1B, 0x00, 0x17, 0x00],
	0x00BC: [0x00, 0x17, 0x0A, 0x1B, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x45, 0x00, 0x13, 0x0B],
	0x00BD: [0x00, 0x13, 0x0B, 0x29, 0x00, 0x16, 0x00, 0x00, 0x00, 0x4F, 0x9E, 0x00, 0x13, 0x0B],
	0x00BE: [0x00, 0x13, 0x0B, 0x29, 0x00, 0x16, 0x00, 0x00, 0x00, 0x4F, 0x9E, 0x00, 0x13, 0x0B],
	0x00BF: [0x00, 0x13, 0x0B, 0x29, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x27, 0x00, 0x02, 0x0F],
	0x00C0: [0x01, 0x00, 0x02, 0x27, 0x00, 0x02, 0x0F, 0x00, 0x00, 0x00, 0xB0, 0xD0, 0x00, 0x11],
	0x00C1: [0x00, 0x11, 0x0C, 0x1D, 0x00, 0x33, 0x00, 0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x27, 0x00],
	0x00C2: [0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x27, 0x00, 0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00],
	0x00C3: [0xC0, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00, 0x00, 0x18, 0x0D, 0x25, 0x00, 0x00, 0x00],
	0x00C4: [0x00, 0x18, 0x0D, 0x25, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB4, 0x00, 0x18, 0x0D],
	0x00C5: [0x00, 0x18, 0x0D, 0x25, 0x00, 0x00, 0x00, 0x00, 0x18, 0x0D, 0x1E, 0x00, 0x33, 0x00],
	0x00C6: [0x00, 0x18, 0x0D, 0x1E, 0x00, 0x00, 0x00, 0x20, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00],
	0x00C7: [0x00, 0x18, 0x0D, 0x1E, 0x00, 0x33, 0x00, 0x00, 0x0B, 0x05, 0x09, 0x00, 0x15, 0x25],
	0x00C8: [0x00, 0x0B, 0x05, 0x09, 0x00, 0x15, 0x25, 0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00],
	0x00C9: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00, 0xC0, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00],
	0x00CA: [0xC0, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00, 0x20, 0x13, 0x0B, 0x29, 0x00, 0x14, 0x00],
	0x00CB: [0xC0, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00, 0x20, 0x13, 0x0B, 0x29, 0x00, 0x14, 0x00],
	0x00CC: [0xC0, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00, 0x20, 0x13, 0x0B, 0x29, 0x00, 0x14, 0x00],
	0x00CD: [0x20, 0x13, 0x0B, 0x29, 0x00, 0x14, 0x00, 0x00, 0x00, 0xDE, 0x01, 0x00, 0x02, 0x21],
	0x00CE: [0x20, 0x13, 0x0B, 0x29, 0x00, 0x14, 0x00, 0x00, 0x00, 0xDE, 0x01, 0x00, 0x02, 0x21],
	0x00CF: [0x01, 0x00, 0x02, 0x21, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0xC0, 0xE0, 0x00, 0x11],
	0x00D0: [0x01, 0x00, 0x02, 0x21, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0xC0, 0xE0, 0x00, 0x11],
	0x00D1: [0x00, 0x11, 0x0C, 0x1D, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB1, 0x97, 0x00, 0x11, 0x0C],
	0x00D2: [0x00, 0x11, 0x0C, 0x1D, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x98, 0x00, 0x0B, 0x05],
	0x00D3: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x06, 0x00, 0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00],
	0x00D4: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x06, 0x00, 0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00],
	0x00D5: [0x00, 0x18, 0x0D, 0x25, 0x00, 0x00, 0x00, 0x00, 0x18, 0x0D, 0x1E, 0x00, 0x33, 0x00],
	0x00D6: [0x00, 0x18, 0x0D, 0x1E, 0x00, 0x00, 0x00, 0x20, 0x18, 0x0D, 0x26, 0x00, 0x00, 0x00],
	0x00D7: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x06, 0x00, 0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00],
	0x00D8: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x06, 0x00, 0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00],
	0x00D9: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00, 0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00],
	0x00DA: [0x00, 0x0B, 0x05, 0x08, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x99, 0xE0, 0x14, 0x0B],
	0x00DB: [0xC0, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00, 0x20, 0x13, 0x0B, 0x29, 0x00, 0x14, 0x00],
	0x00DC: [0xC0, 0x17, 0x0A, 0x1B, 0x00, 0x00, 0x00, 0x20, 0x13, 0x0B, 0x29, 0x00, 0x14, 0x00],
	0x00DD: [0xE0, 0x14, 0x0B, 0x16, 0x00, 0x25, 0x00, 0xC0, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00DE: [0xE0, 0x14, 0x0B, 0x16, 0x00, 0x25, 0x00, 0xC0, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00DF: [0xC0, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEF, 0x00, 0x26, 0x02],
	0x00E0: [0x00, 0x26, 0x02, 0x21, 0x00, 0x01, 0x2A, 0x00, 0x00, 0x00, 0xD0, 0xC0, 0x07, 0x06],
	0x00E1: [0xC0, 0x07, 0x06, 0x28, 0x00, 0x00, 0x00, 0x00, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00E2: [0x00, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0xC0, 0x20, 0x06, 0x09, 0x00, 0x00, 0x00],
	0x00E3: [0xC0, 0x20, 0x06, 0x09, 0x00, 0x00, 0x00, 0x01, 0x07, 0x14, 0x01, 0x00, 0x00, 0x00],
	0x00E4: [0x01, 0x07, 0x14, 0x01, 0x00, 0x00, 0x00, 0x01, 0x07, 0x06, 0x01, 0x00, 0x00, 0x00],
	0x00E5: [0x01, 0x07, 0x14, 0x01, 0x00, 0x00, 0x00, 0x01, 0x07, 0x06, 0x01, 0x00, 0x00, 0x00],
	0x00E6: [0x01, 0x07, 0x06, 0x01, 0x00, 0x00, 0x00, 0x20, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00E7: [0x01, 0x07, 0x06, 0x01, 0x00, 0x00, 0x00, 0x20, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00E8: [0x20, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8],
	0x00E9: [0x20, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFA, 0xFA, 0x20, 0x07, 0x06],
	0x00EA: [0x20, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFA, 0xFA, 0x20, 0x07, 0x06],
	0x00EB: [0x20, 0x07, 0x06, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFB, 0xFB, 0x20, 0x20, 0x06],
	0x00EC: [0x20, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFD, 0xFD, 0xFD, 0x20, 0x20],
	0x00ED: [0x20, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFD, 0xFD, 0xFD, 0x20, 0x20],
	0x00EE: [0x20, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFE, 0x20, 0x20, 0x06, 0x13],
	0x00EF: [0x20, 0x20, 0x06, 0x13, 0x00, 0x02, 0x00, 0x08, 0x00, 0xFF, 0xDF, 0xFF, 0x00, 0x02],
	0x00F0: [0x01, 0x07, 0x06, 0x01, 0x00, 0x00, 0x00, 0x20, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00F1: [0x01, 0x07, 0x06, 0x01, 0x00, 0x00, 0x00, 0x20, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00F2: [0x00, 0x02, 0x03, 0x05, 0x00, 0x00, 0x02, 0x03, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x07],
	0x00F3: [0x00, 0x02, 0x03, 0x05, 0x00, 0x00, 0x02, 0x03, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x07],
	0x00F4: [0x00, 0x02, 0x03, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00F5: [0x00, 0x02, 0x03, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00F6: [0x00, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE8, 0xE8, 0xE8, 0xE8],
	0x00F7: [0x00, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE8, 0xE8, 0xE8, 0xE8],
	0x00F8: [0x00, 0x07, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE8, 0xE8, 0xE8, 0xE8],
	0x00F9: [0x00, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0xC0, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00FA: [0xC0, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEA, 0x00, 0x07, 0x06],
	0x00FB: [0x00, 0x07, 0x06, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEB, 0x00, 0x20, 0x06],
	0x00FC: [0x00, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xED, 0xED, 0x00, 0x07],
	0x00FD: [0x00, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xED, 0xED, 0x00, 0x07],
	0x00FE: [0x00, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00, 0xC0, 0x20, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x00FF: [0x00, 0x07, 0x06, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEF, 0x00, 0x05, 0x03],
	0x0100: [0x00, 0x05, 0x03, 0x28, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x03, 0x05, 0x00, 0x00, 0x00],
	0x0101: [0x00, 0x02, 0x03, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x15, 0x03, 0x0D, 0x00, 0x00, 0x00],
	0x0102: [0x00, 0x15, 0x03, 0x0D, 0x00, 0x00, 0x00, 0x00, 0x05, 0x03, 0x0F, 0x00, 0x00, 0x00],
	0x0103: [0x00, 0x05, 0x03, 0x0F, 0x00, 0x00, 0x00, 0x01, 0x15, 0x03, 0x0D, 0x00, 0x00, 0x00],
	0x0104: [0x01, 0x15, 0x03, 0x0D, 0x00, 0x00, 0x00, 0x00, 0x1C, 0x0F, 0x10, 0x00, 0x00, 0x00],
	0x0105: [0x00, 0x1C, 0x0F, 0x10, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x03, 0x0F, 0x00, 0x00, 0x00],
	0x0106: [0x00, 0x1F, 0x03, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x02, 0x03, 0x01, 0x00, 0x00, 0x00],
	0x0107: [0x00, 0x02, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x02, 0x03, 0x0E, 0x00, 0x00, 0x00],
	0x0108: [0x00, 0x02, 0x03, 0x0E, 0x00, 0x00, 0x00, 0x01, 0x05, 0x03, 0x05, 0x00, 0x00, 0x00],
	0x0109: [0x01, 0x05, 0x03, 0x05, 0x00, 0x00, 0x00, 0x01, 0x07, 0x06, 0x10, 0x00, 0x00, 0x00],
	0x010A: [0x01, 0x07, 0x06, 0x10, 0x00, 0x00, 0x00, 0x80, 0x0A, 0x08, 0x08, 0x00, 0x00, 0x1A],
	0x010B: [0x80, 0x0A, 0x08, 0x08, 0x00, 0x00, 0x1A, 0x00, 0x27, 0x06, 0x08, 0x00, 0x03, 0x00],
	0x010C: [0x00, 0x27, 0x06, 0x08, 0x00, 0x03, 0x00, 0x00, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00],
	0x010D: [0x00, 0x0A, 0x08, 0x11, 0x00, 0x00, 0x00, 0x00, 0x07, 0x14, 0x05, 0x00, 0x00, 0x00],
	0x010E: [0x00, 0x07, 0x14, 0x05, 0x00, 0x00, 0x00, 0x00, 0x1E, 0x11, 0x05, 0x00, 0x00, 0x00],
	0x010F: [0x00, 0x1F, 0x03, 0x05, 0x00, 0x00, 0x00, 0x00, 0x02, 0x03, 0x0F, 0x00, 0x00, 0x00],
	0x0110: [0x00, 0x1F, 0x03, 0x05, 0x00, 0x00, 0x00, 0x00, 0x02, 0x03, 0x0F, 0x00, 0x00, 0x00],
	0x0111: [0x00, 0x1E, 0x11, 0x05, 0x00, 0x00, 0x00, 0x00, 0x07, 0x14, 0x05, 0x00, 0x00, 0x00],
	0x0112: [0x00, 0x07, 0x14, 0x05, 0x00, 0x00, 0x00, 0x00, 0x03, 0x10, 0x08, 0x00, 0x00, 0x00],
	0x0113: [0x00, 0x03, 0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x07, 0x06, 0x07, 0x00, 0x00, 0x00],
	0x0114: [0x00, 0x07, 0x06, 0x07, 0x00, 0x00, 0x00, 0x00, 0x22, 0x12, 0x07, 0x00, 0x00, 0x00],
	0x0115: [0x00, 0x07, 0x06, 0x07, 0x00, 0x00, 0x00, 0x00, 0x22, 0x12, 0x07, 0x00, 0x00, 0x00],
	0x0116: [0x00, 0x22, 0x12, 0x07, 0x00, 0x00, 0x00, 0x00, 0x20, 0x14, 0x05, 0x00, 0x00, 0x00],
	0x0117: [0x00, 0x20, 0x14, 0x05, 0x00, 0x00, 0x00, 0xE0, 0x23, 0x0A, 0x0F, 0x00, 0x00, 0x00],
	0x0118: [0x00, 0x05, 0x03, 0x0F, 0x00, 0x00, 0x00, 0x01, 0x15, 0x03, 0x0D, 0x00, 0x00, 0x00],
	0x0119: [0xE0, 0x23, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1D, 0x00, 0x1C, 0x0F],
	0x011A: [0x00, 0x1C, 0x0F, 0x05, 0x00, 0x00, 0x00, 0xC0, 0x07, 0x06, 0x08, 0x00, 0x00, 0x00],
	0x011B: [0xC0, 0x07, 0x06, 0x08, 0x00, 0x00, 0x00, 0x00, 0x23, 0x0A, 0x0F, 0x00, 0x00, 0x00],
	0x011C: [0x00, 0x1F, 0x03, 0x05, 0x00, 0x00, 0x00, 0x00, 0x02, 0x03, 0x0F, 0x00, 0x00, 0x00],
	0x011D: [0x00, 0x23, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x19, 0x00, 0x20, 0x06],
	0x011E: [0x00, 0x20, 0x06, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x05, 0x03, 0x05, 0x00, 0x00, 0x00],
	0x011F: [0x00, 0x05, 0x03, 0x05, 0x00, 0x00, 0x00, 0x00, 0x13, 0x06, 0x13, 0x00, 0x00, 0x00],
	0x0120: [0x00, 0x13, 0x06, 0x13, 0x00, 0x00, 0x00, 0x00, 0x07, 0x06, 0x28, 0x00, 0x03, 0x00],
	0x0121: [0x00, 0x1E, 0x11, 0x05, 0x00, 0x00, 0x00, 0x00, 0x07, 0x14, 0x05, 0x00, 0x00, 0x00],
	0x0122: [0x00, 0x1E, 0x11, 0x05, 0x00, 0x00, 0x00, 0x00, 0x07, 0x14, 0x05, 0x00, 0x00, 0x00],
	0x0123: [0x00, 0x07, 0x06, 0x28, 0x00, 0x03, 0x00, 0x00, 0x07, 0x06, 0x28, 0x00, 0x00, 0x00],
	0x0124: [0x00, 0x07, 0x06, 0x28, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x0125: [0x00, 0x07, 0x06, 0x28, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x0126: [0x00, 0x07, 0x06, 0x28, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x0127: [0x00, 0x20, 0x06, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x05, 0x03, 0x05, 0x00, 0x00, 0x00],
	0x0128: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x0129: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x012A: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x012B: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x012C: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x012D: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
	0x012E: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
}


class RoomHeader:
	def __init__(self, room_id, byte_array):
		self.room_id = room_id

		# todo: the rest of the header
		self.byte_0 = byte_array[0]  # bg2, collision, lights out
		self.sprite_sheet = byte_array[3]  # sprite gfx #
		self.effect = byte_array[4]

	def write_to_rom(self, rom, base_address):
		room_offest = self.room_id*14
		rom.write_byte(base_address + room_offest + 0, self.byte_0)
		rom.write_byte(base_address + room_offest + 3, self.sprite_sheet)
		rom.write_byte(base_address + room_offest + 4, self.effect)


def init_room_headers():
	header_table = {}
	for room_id, header_bytes in vanilla_headers.items():
		header_table[room_id] = RoomHeader(room_id, header_bytes)
	return header_table
