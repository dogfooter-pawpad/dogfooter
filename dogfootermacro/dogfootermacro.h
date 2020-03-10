#ifndef DOGFOOTERMACRO_H
#define DOGFOOTERMACRO_H

#include <QMainWindow>

namespace Ui {
class DogfooterMacro;
}

class DogfooterMacro : public QMainWindow
{
    Q_OBJECT

public:
    explicit DogfooterMacro(QWidget *parent = nullptr);
    ~DogfooterMacro();

private:
    Ui::DogfooterMacro *ui;
};

#endif // DOGFOOTERMACRO_H
