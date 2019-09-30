import tkinter
import threading
import likeyoubot_configure
import sys
import pickle
import os
import likeyoubot_login_gui
import likeyoubot_logger

def connresize(e):
    global configure

    if e.width == configure.w and e.height == configure.h and e.x != 0 and e.y != 0:
        if e.x != configure.x or e.y != configure.y:
            configure.x = e.x
            configure.y = e.y
            try:
                with open(resource_path('lyb.cfg'), 'wb') as dat_file:
                    pickle.dump(configure, dat_file)
            except:
                print('connresize: ' + str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')


def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )


try:
    dogfooter_logger = likeyoubot_logger.LYBLogger.getLogger()
except:
    print('create logger fail: ' + str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')
    sys.exit(1)

threading.currentThread().setName('UI')
dogfooter_logger.info('Dogfooter ' + likeyoubot_configure.LYBConstant.LYB_VERSION)

configure = None
root = tkinter.Tk()
root.resizable(width=False, height=False)
# root.overrideredirect(True)
root.iconbitmap(resource_path('images/dogfooterbot_icon.ico'))
root.bind("<Configure>", connresize)

# TODO: 설정 파일 읽어오기
try:
    with open(resource_path('lyb.cfg'), 'rb') as dat_file:
        configure = pickle.load(dat_file)
        if configure.getGeometryLogin() == None:
            w = 320
            h = 200
            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            configure.setGeometryLogin(w, h, x, y)

    root.geometry('%dx%d+%d+%d' % configure.getGeometryLogin())

    configure.path = resource_path('lyb.cfg')
    dogfooter_logger.debug('configure.path [' + configure.path + ']')
except FileNotFoundError:
    w = 320
    h = 200
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    configure = likeyoubot_configure.LYBConfigure(x, y, w, h, 'MOMO|Nox', resource_path('lyb.cfg'))
    configure.setGeometryLogin(w, h, x, y)
    configure.setGeometry(800, 640, x, y)
    try:
        with open(resource_path('lyb.cfg'), 'wb') as dat_file:
            pickle.dump(configure, dat_file)
    except:
        dogfooter_logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')

except:
    dogfooter_logger.error(str(sys.exc_info()[0]) + '(' + str(sys.exc_info()[1]) + ')')

try:
    with open(resource_path('host'), 'r') as host_file:
        configure.root_url = host_file.readline()
except FileNotFoundError:
    configure.root_url = 'https://pawpad.kr'

configure.merge()
root.update()

# if lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove' in configure.common_config:
# 	if configure.common_config[lybconstant.LYB_DO_BOOLEAN_LOG_LEVEL + 'remove'] == True:
likeyoubot_logger.LYBLogger.removeLog()

dogfooter_logger.debug('size: ' + str(root.winfo_width()) + ' ' + str(root.winfo_height()))
# lyb_gui = likeyoubot_gui.LYBGUI(root, configure)
likeyoubot_login_gui.LYBLoginGUI(root, configure)

root.mainloop()
