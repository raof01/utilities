import { Injectable } from '@angular/core';
import { Store } from '@gnrx/store';
import { Observable } from 'rxjs/Rx';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { DbProxy } from './db.proxy';
import { DbConnModel } from './db.models';
import { DbActions } from '../actions/db.actions';
import { DbRepository } from './db.repository';
import { DbState } from './db.models';

@Injectable()
export class DbService {

    private state: Observable<DbState>;

    constructor(
        private http: Http,
        private proxyService: DbProxy,
        private dbActions: DbActions,
        private dbRepository: DbRepository,
        private store: Store<any>
    ) {
        this.state = this.store.select('dbReducer') as Observable<DbState>;
    }

    public setDbConn(dbConnModel: DbConnModel) {
        this.store.dispatch(this.dbActions.setDbConn(dbConnModel));
    }

    private getDbConn(): Observable<DbConnModel> {
        return this.state.map((v: DbState) => {
            return v.dbConn;
        });
    }
/*
    public getDbs(): Observable<string[]> {
        this.getDbConn().subscribe((v: DbConnModel) => {
            this.dbRepository.getDbs(v).subscribe((v: string[]) => {
                this.store.dispatch(this.dbActions.addDbs(v));
            });
        });
        return this.state.map((v: DbState) => {
            return v.dbs;
        });
    }
*/
    /*
     * TODO
     * To move to DbRepository
     */
    public getDbs(dbConnModel: DbConnModel) : void {
        /*let body: string = `{
            host: ${ip},
            port: ${port},
            user: ${user},
            password: ${password}
        }`;*/
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}`;
        this.http.get(`${dbConnModel.url}dbs?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyDbs(value.json());
        });
    }

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
