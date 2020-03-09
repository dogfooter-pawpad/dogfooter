#include "dogfootermacro.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    DogfooterMacro w;
    w.show();

    return a.exec();
}
