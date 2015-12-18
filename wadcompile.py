# wadcompile
import sys, omg, os, omg.txdef
from PIL import Image

def dir_compile(dir_path, outpath = None):
    outwad = omg.WAD()
    name = dir_path
    if '/' in name:
        name = name[name.rfind('/')+1:]
    if '\\' in name:
        name = name[name.rfind('\\')+1:]

    tex_path = dir_path + "/textures"
    flat_path = dir_path + "/flats"

    tex_list = []
    flat_list = []

    for file in os.listdir(tex_path):
        if file.endswith(".png"):
            tex_list.append(str(file))

    for file in os.listdir(flat_path):
        if file.endswith(".png"):
            flat_list.append(str(file))

    txd = omg.txdef.Textures()

    for t in tex_list:
        tname = t[:t.rfind('.')]
        patch = omg.Graphic()
        timg = Image.open(tex_path+"\\"+t)
        pink = Image.new("RGB",timg.size,'#ff00ff')
        pink.paste(timg,None)
        timg = pink.convert('RGB')
        # if tname == "AQMETL18":
        #     pink.show()
        #     timg.show()
        patch.from_Image(timg)
        outwad.patches[tname] = patch
        txd[tname] = omg.txdef.TextureDef()
        txd[tname].name = tname
        txd[tname].patches.append(omg.txdef.PatchDef())
        txd[tname].patches[0].name = tname
        txd[tname].width, txd[tname].height = patch.dimensions

    for f in flat_list:
        fname = f[:t.rfind('.')]
        flat = omg.Flat()
        fimg = Image.open(flat_path+"/"+f)
        fimg = fimg.convert('RGB')
        flat.from_Image(fimg)
        outwad.flats[fname] = flat

    outwad.txdefs = txd.to_lumps()

    if outpath is None:
        outpath = os.path.abspath(os.path.join(dir_path, os.pardir)) + "\\" + name + ".wad"
    outwad.to_file(outpath)


if __name__=="__main__":
    if len(sys.argv) <= 1:
        print("usage:")
        print("    wadcompile [directory_path]")

    dir_path = sys.argv[1]
    dir_compile(dir_path)