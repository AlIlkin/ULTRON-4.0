#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main() {
    char degtype, ch;
    double fahrenheit, celsius, kelvin;

    printf("Enter the degree type: ");
    scanf(" %c", &degtype);

    if (degtype == 'f' || degtype == 'F')
    {
        printf("Celsius (C) or Kelvin (K)?: ");
        scanf(" %c", &ch);
        switch (ch) {
        case 'C':
        case 'c':printf("Celsius: ");
            scanf("%lf", &celsius);
            fahrenheit = (celsius * 9 / 5) + 32;
            printf("%.2f degrees Fahrenheit\n", fahrenheit);
            break;
        case 'K':
        case 'k':printf("Kelvin: ");
            scanf("%lf", &kelvin);
            fahrenheit = ((kelvin - 273.15) * 9 / 5) + 32;
            printf("%.2f degrees Fahrenheit\n", fahrenheit);
            break;
        }
    }
    else if (degtype == 'c' || degtype == 'C')
    {
        printf("Fahrenheit (F) or Kelvin (K)?: ");
        scanf(" %c", &ch);
        switch (ch) {
        case 'F':
        case 'f':printf("Fahrenheit: ");
            scanf("%lf", &fahrenheit);
            celsius = (fahrenheit - 32) * 5 / 9;
            printf("%.2f degrees Celsius\n", celsius);
            break;
        case 'K':
        case 'k':printf("Kelvin: ");
            scanf("%lf", &kelvin);
            celsius = kelvin - 273.15;
            printf("%.2f degrees Celsius\n", celsius);
            break;
        }
    }
    else if (degtype == 'k' || degtype == 'K') {
        printf("Celsius (C) or Fahrenheit (F)?: ");
        scanf(" %c", &ch);
        switch (ch) {
        case 'C':
        case 'c':printf("Celsius: ");
            scanf("%lf", &celsius);
            kelvin = celsius + 273.15;
            printf("%.2f degrees Kelvin\n", kelvin);
            break;
        case 'F':
        case 'f':printf("Fahrenheit: ");
            scanf("%lf", &fahrenheit);
            kelvin = ((fahrenheit - 32) * 5 / 9) + 273.15;
            printf("%.2f degrees Kelvin\n", kelvin);
            break;
        }
    }
    else{
        printf("Are you dumb?\nAre you too stupid to choose one letter among three?\nThere are three letters!\nF, C, or K..."); 
    }
    return 0;
}
