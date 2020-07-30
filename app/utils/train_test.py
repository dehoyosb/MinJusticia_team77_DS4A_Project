# Train and test sets
def train_test(inmate, train_start, train_end, test_start, test_end, month):
    # Generate train and test data frames
    dftrain = inmate.copy()[(inmate.year >= train_start) & (inmate.year <= train_end)]
    dftest  = inmate.copy()[(inmate.year >= test_start ) & (inmate.year <= test_end )]

    # Calculate age based on train and test end period
    dftrain['age'] = train_end - dftrain.ANIO_NACIMIENTO
    dftest['age']  = test_end  - dftest .ANIO_NACIMIENTO

    # Calculate outcome variable = 1 if individual came to jail in less that a year
    dftrain['outcome'] = (dftrain.recidivism_day <= month*30).astype(int)
    dftest['outcome']  = (dftest.recidivism_day  <= month*30).astype(int)
    
    # Number of individuals that came back to jail in less than a year
    print('Train set: {} out of {} ~ {}%'.format(dftrain.outcome.sum(),
                                                 dftrain.shape[0],round(dftrain.outcome.sum()*100/dftrain.shape[0])))
    print('Test  set: {} out of {} ~ {}%'.format(dftest.outcome.sum(),
                                                 dftest.shape[0],round(dftest.outcome.sum()*100/dftest.shape[0])))
    
    # Drop unnecesary features
    colnmes = dftrain.columns.drop(['ANIO_NACIMIENTO',
                                    'FECHA_SALIDA_t_1',
                                    'FECHA_INGRESO',
                                    'FECHA_SALIDA',
                                    'INTERNOEN',
                                    'year',
                                    'recidivism_day',
                                    'outcome']).tolist()
    
    # Create train and test sets 
    X_train, y_train = dftrain[colnmes], dftrain['outcome']
    X_test , y_test  = dftest [colnmes], dftest ['outcome']
    
    return X_train, y_train, X_test, y_test