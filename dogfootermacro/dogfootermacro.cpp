#include "dogfootermacro.h"
#include "ui_dogfootermacro.h"

DogfooterMacro::DogfooterMacro(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::DogfooterMacro)
{
    ui->setupUi(this);
}

DogfooterMacro::~DogfooterMacro()
{
    delete ui;
}
