import { Injectable } from '@angular/core';
import { Action, createAction } from 'redux-actions';

import { DbConnModel } from '../db/db.models';

@Injectable()
export class ConnActions {
    public static SET_CONN: string = '[connReducer] Set Connection';
    public setDbConn: (dbConn: any) => Action<any> = createAction(ConnActions.SET_CONN);
}
