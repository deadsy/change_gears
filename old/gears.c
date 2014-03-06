/************************************************************************************/
/*

Copyright Jason T. Harris 2004. All rights reserved.

Calculate Change Gears for a 8x14 Lathe.

*/
/************************************************************************************/
// Includes

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/************************************************************************************/
// Gear Configurations

enum
{
    GEAR_CONFIG_0,    // A to B to C
    GEAR_CONFIG_1,    // AB to CD to E
    GEAR_CONFIG_2,    // AB to C to D
    GEAR_CONFIG_3,    // A to BC to D
    GEAR_CONFIG_MAX   // must be last
};

/************************************************************************************/
// Geometric Constants

#define MM_PER_INCH    25.4
#define PI             3.1415926535
#define IDLER_TEETH    40.0
#define LEADSCREW_TPI  12.0
#define GEAR_PITCH     0.125

/************************************************************************************/
// Geometric Constraints

#define MINIMUM_GTL            154  // Minimum gear train length
#define MIN_FINAL_GEARS        80   // Minimum center to center for final 2 gears
#define MAX_AB_DIFFERENCE      6    // Maximum AB difference for gear configs 1 & 2
#define MIN_GEAR_CLEARANCE     4    // Minimum gear to gear clearance
#define GEAR_X_SIZE            30   // Size of a hub with no gear present
#define MAX_SLOT_GEARS         168  // Maximum length for engaged gears in the slot

/************************************************************************************/
// Gear Set

static int gear_set[] =
{
    30, 35, 40, 45, 48, 50, 60, 66,
    68, 70, 70, 72, 75, 80, 90, 100
};

#define NUM_GEARS (sizeof(gear_set) / sizeof(int))

/************************************************************************************/
// Gear Solutions

#define INITIAL_ERROR 1.0

typedef struct
{
    double error;

    int a;
    int b;
    int c;
    int d;
    int e;

} GS;

static GS soln[ GEAR_CONFIG_MAX ];

/************************************************************************************/
// Variables

static double goal_pitch;
static int valid_count = 0;
static int vec[ 10 ];

/************************************************************************************/
// Return the screw pitch in inches

static double Calc_Pitch( int cfg, int ga, int gb, int gc, int gd, int ge )
{
    double ratio;

    ratio = IDLER_TEETH / (double)ga;

    switch( cfg )
    {
        case GEAR_CONFIG_0:
        {
            ratio *= ( (double)ga / (double)gc );
            break;
        }

        case GEAR_CONFIG_1:
        {
            ratio *= ( (double)gb / (double)gc );
            ratio *= ( (double)gd / (double)ge );
            break;
        }

        case GEAR_CONFIG_2:
        {
            ratio *= ( (double)gb / (double)gd );
            break;
        }

        case GEAR_CONFIG_3:
        {
            ratio *= ( (double)ga / (double)gb );
            ratio *= ( (double)gc / (double)gd );
            break;
        }

        default:
        {
            assert( 0 );
        }
    }

    return ratio / LEADSCREW_TPI;
}

/************************************************************************************/
// Return the gear train length in teeth

static int Calc_Length( int cfg, int ga, int gb, int gc, int gd, int ge )
{
    int length;

    length = IDLER_TEETH / 2;

    switch( cfg )
    {
        case GEAR_CONFIG_0:
        {
            length += (double)ga;
            length += (double)gb;
            length += (double)gc / 2;
            break;
        }

        case GEAR_CONFIG_1:
        {
            length += (double)ga / 2;
            length += (double)gb / 2;
            length += (double)gc / 2;
            length += (double)gd / 2;
            length += (double)ge / 2;
            break;
        }

        case GEAR_CONFIG_2:
        {
            length += (double)ga / 2;
            length += (double)gb / 2;
            length += (double)gc;
            length += (double)gd / 2;
            break;
        }

        case GEAR_CONFIG_3:
        {
            length += (double)ga;
            length += (double)gb / 2;
            length += (double)gc / 2;
            length += (double)gd / 2;
            break;
        }

        default:
        {
            assert( 0 );
        }
    }

    return length;
}

/************************************************************************************/

static void Display_Gears(int cfg, int mode)
{
    int ga, gb, gc, gd, ge;
    double pitch, error;

    error = ( soln[ cfg ].error / goal_pitch ) * 100.0;

    ga = soln[cfg].a;
    gb = soln[cfg].b;
    gc = soln[cfg].c;
    gd = soln[cfg].d;
    ge = soln[cfg].e;

    pitch = Calc_Pitch(cfg, ga, gb, gc, gd, ge);

    if (mode != 0) {
        printf( "desired tpi = %f\n", ( 1.0 / goal_pitch ) );
        printf( "actual tpi = %f\n", ( 1.0 / pitch ) );
    } else {
        printf( "desired pitch = %f mm\n", goal_pitch * MM_PER_INCH );
        printf( "actual pitch = %f mm\n", pitch * MM_PER_INCH );
    }

    printf( "pitch error = %.2f%%\n", error );

    switch (cfg) {
        case GEAR_CONFIG_0: {
            printf( "%d-%d-%d\n", ga, gb, gc );
            break;
        }
        case GEAR_CONFIG_1: {
            printf( "%d:%d-%d:%d-%d\n", ga, gb, gc, gd, ge );
            break;
        }
        case GEAR_CONFIG_2: {
            printf( "%d:%d-%d-%d\n", ga, gb, gc, gd );
            break;
        }
        case GEAR_CONFIG_3: {
            printf( "%d-%d:%d-%d\n", ga, gb, gc, gd );
            break;
        }
        default: {
            assert( 0 );
        }
    }

    printf( "\n" );
}

/************************************************************************************/

static void Display_Gears_HTML( int cfg, int mode )
{
    int ga, gb, gc, gd, ge;
    double pitch, error;

    error = ( soln[ cfg ].error / goal_pitch ) * 100.0;

    ga = soln[ cfg ].a;
    gb = soln[ cfg ].b;
    gc = soln[ cfg ].c;
    gd = soln[ cfg ].d;
    ge = soln[ cfg ].e;

    pitch = Calc_Pitch( cfg, ga, gb, gc, gd, ge );

    printf( "<tr>" );

    if( mode != 0 )
    {
        printf( "<td>%.2f</td>", ( 1.0 / goal_pitch ) );
        printf( "<td>%.3f</td>", ( 1.0 / pitch ) );
    }
    else
    {
        printf( "<td>%.2f</td>", goal_pitch * MM_PER_INCH );
        printf( "<td>%.3f</td>", pitch * MM_PER_INCH );
    }

    printf( "<td>%.2f%%</td>", error );

    printf( "<td>" );

    switch( cfg )
    {
        case GEAR_CONFIG_0:
        {
            printf( "%d-%d-%d", ga, gb, gc );
            break;
        }

        case GEAR_CONFIG_1:
        {
            printf( "%d:%d-%d:%d-%d", ga, gb, gc, gd, ge );
            break;
        }

        case GEAR_CONFIG_2:
        {
            printf( "%d:%d-%d-%d", ga, gb, gc, gd );
            break;
        }

        case GEAR_CONFIG_3:
        {
            printf( "%d-%d:%d-%d", ga, gb, gc, gd );
            break;
        }

        default:
        {
            assert( 0 );
        }
    }

    printf( "</td></tr>\n" );
}

/************************************************************************************/
// Is this a geometrically valid gear configuration?

static int Gear_Valid( int cfg, int ga, int gb, int gc, int gd, int ge )
{
    switch( cfg ) {
        case GEAR_CONFIG_0: {
            if ((ga + gb) > MAX_SLOT_GEARS) {
                return 0;
            }
            if( ( gb + gc ) < MIN_FINAL_GEARS) {
                return 0;
            }
            break;
        }

        case GEAR_CONFIG_1: {
            if( ( gb + gc ) > MAX_SLOT_GEARS ) {
                return 0;
            }

            if( ( gd + ge ) < MIN_FINAL_GEARS ) {
                return 0;
            }

            if ( ( gb - ga ) > MAX_AB_DIFFERENCE ) {
                return 0;
            }

            if( ( gb + gc ) - ( ga + gd ) < MIN_GEAR_CLEARANCE ) {
                return 0;
            }

            if( ( gd + ge ) - ( gc + GEAR_X_SIZE ) < MIN_GEAR_CLEARANCE ) {
                return 0;
            }

            break;
        }

        case GEAR_CONFIG_2:
        {
            if( ( gb + gc ) > MAX_SLOT_GEARS )
            {
                return 0;
            }

            if( ( gc + gd ) < MIN_FINAL_GEARS )
            {
                return 0;
            }

            if( ( gb - ga ) > MAX_AB_DIFFERENCE )
            {
                return 0;
            }

            break;
        }

        case GEAR_CONFIG_3:
        {
            if( ( ga + gb ) > MAX_SLOT_GEARS )
            {
                return 0;
            }

            if( ( gc + gd ) < MIN_FINAL_GEARS )
            {
                return 0;
            }

            if( ( ga + gb ) - ( gc + GEAR_X_SIZE ) < MIN_GEAR_CLEARANCE )
            {
                return 0;
            }

            if( ( gc + gd ) - ( gb + GEAR_X_SIZE ) < MIN_GEAR_CLEARANCE )
            {
                return 0;
            }

            break;
        }

        default:
        {
            assert( 0 );
        }
    }

    if( Calc_Length( cfg, ga, gb, gc, gd, ge ) < MINIMUM_GTL )
    {
        return 0;
    }

    return 1;
}

/************************************************************************************/

static void Check_Gears( int cfg )
{
    int ga, gb, gc, gd, ge;

    ga = gear_set[ vec [ 0 ] ];
    gb = gear_set[ vec [ 1 ] ];
    gc = gear_set[ vec [ 2 ] ];
    gd = gear_set[ vec [ 3 ] ];
    ge = gear_set[ vec [ 4 ] ];

    if( Gear_Valid( cfg, ga, gb, gc, gd, ge ) != 0 )
    {
        double error, pitch;

        valid_count ++;

        pitch = Calc_Pitch( cfg, ga, gb, gc, gd, ge );
        error = fabs( pitch - goal_pitch );

        if( error < soln[ cfg ].error )
        {
            soln[ cfg ].error = error;
            soln[ cfg ].a = ga;
            soln[ cfg ].b = gb;
            soln[ cfg ].c = gc;
            soln[ cfg ].d = gd;
            soln[ cfg ].e = ge;
        }
    }
}

/************************************************************************************/

static void swap( int i, int j )
{
    int tmp = vec[ i ];
    vec[ i ] = vec[ j ];
    vec[ j ] = tmp;
}

/************************************************************************************/

static void Permute_Gears( int cfg, int n )
{
    int i;

    if( n == 0 )
    {
        Check_Gears( cfg );
        return;
    }

    for( i = 0; i <= n; i ++ )
    {
        swap( n, i );
        Permute_Gears( cfg, n - 1 );
        swap( n, i );
    }
}

/************************************************************************************/

static void Combine_Gears( int ix, int kx,  int n, int k )
{
    int i;

    if( kx == 3 )
    {
        Permute_Gears( GEAR_CONFIG_0, 2 );
    }

    if( kx == 4 )
    {
        Permute_Gears( GEAR_CONFIG_2, 3 );
        Permute_Gears( GEAR_CONFIG_3, 3 );
    }

    if( kx == k )
    {
        Permute_Gears( GEAR_CONFIG_1, 4 );
        return;
    }

    for( i = ix; i <= n; i ++ )
    {
        vec[ kx ] = i;
        Combine_Gears( i + 1, kx + 1, n, k );
    }
}

/************************************************************************************/

void Search_Gears(int mode)
{
    int i, best;
    double error = INITIAL_ERROR;

    for( i = 0; i < GEAR_CONFIG_MAX; i ++ )
    {
        soln[ i ].error = INITIAL_ERROR;
    }

    Combine_Gears( 0, 0, NUM_GEARS - 1, 5 );

    // Find the best solution

    for( i = 0; i < GEAR_CONFIG_MAX; i ++ )
    {
        if( soln[ i ].error < error )
        {
            error = soln[ i ].error;
            best = i;
        }
    }

    //Display_Gears_HTML( best, mode );
    Display_Gears(best, mode);

    //printf( "Valid Configurations %d\n", valid_count );
}

/************************************************************************************/

int main( int argc, char **argv )
{
    int tpi, mm;

#if 0

    // Inch Sizes
    for (tpi = 7; tpi <= 410; tpi ++) {
        goal_pitch = (1.0 / ((double)tpi / 2.0));
        Search_Gears(1);
    }

    // Metric Sizes
    for (mm = 1; mm <= 75; mm ++) {
        goal_pitch = ((double)mm / 10.0) / MM_PER_INCH;
        Search_Gears(0);
    }

#endif

    goal_pitch = (double)(1.75) / MM_PER_INCH;
    Search_Gears(0);

    exit(0);
}

/************************************************************************************/
