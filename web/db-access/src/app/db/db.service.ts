import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Rx';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { DbProxy } from './db.proxy';
import { DbConnModel } from './db.models';
import { DbActions } from '../actions/db.actions';
import { ConnActions } from '../actions/conn.action';
import { DbRepository } from './db.repository';
import { DbState } from './db.models';

@Injectable()
export class DbService {

    private state: Observable<DbState>;
    private dbConn: Observable<DbConnModel>;

    constructor(
        private http: Http,
        private proxyService: DbProxy,
        private dbActions: DbActions,
        private connActions: ConnActions,
        private dbRepository: DbRepository,
        private store: Store<any>
    ) {
        this.state = this.store.select('dbReducer') as Observable<DbState>;
        this.dbConn = this.store.select('connReducer') as Observable<DbConnModel>;
    }

    public setDbConn(dbConnModel: DbConnModel) {
        this.store.dispatch(this.connActions.setDbConn(dbConnModel));
    }

    public getDbs() {
        this.dbConn.subscribe((v: DbConnModel) => {
            this.dbRepository.getDbs(v).subscribe((value: Response) => {
                this.store.dispatch(this.dbActions.addDbs(value.json()))
                this.proxyService.notifyDbs(value.json());
            });
        });
    }

    /*
     * TODO
     * To move to DbRepository
     
    public getDbs(dbConnModel: DbConnModel) : void {
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}`;
        this.http.get(`${dbConnModel.url}dbs?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyDbs(value.json());
        });
    }*/

    public getTables(dbConnModel: DbConnModel, dbName: string) {
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}&dbName=${dbName}`;
        this.http.get(`${dbConnModel.url}tables?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyTables(value.json());
        });
    }

    public getColumns(dbConnModel: DbConnModel, dbName: string, tblName: string) {
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}&dbName=${dbName}&tableName=${tblName}`;
        this.http.get(`${dbConnModel.url}columns?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyFields(value.json());
        });
    }

    public getValues(dbConnModel: DbConnModel, dbName: string, tblName: string, fields: string[]) {
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}&dbName=${dbName}&tableName=${tblName}&fields=${fields.join(',')}`;
        this.http.get(`${dbConnModel.url}table?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyRows(value.json());
        });
    }
}
