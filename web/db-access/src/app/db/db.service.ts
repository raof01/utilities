import { Injectable, EventEmitter } from '@angular/core';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { Proxy } from '../proxy.service';
@Injectable()
export class DbService {

    constructor(private http: Http, private proxyService: Proxy) {
    }

    public getDbs(url: string, ip: string, port: number, user: string, password: string) : void {
        /*let body: string = `{
            host: ${ip},
            port: ${port},
            user: ${user},
            password: ${password}
        }`;*/
        let query: string =
            `host=${ip}&port=${port}&user=${user}&password=${password}`;
        this.http.get(`${url}dbs?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyDbs(value.json());
        });
    }

    public getTables(url: string, ip: string, port: number, user: string, password: string, dbName: string) {
        let query: string =
            `host=${ip}&port=${port}&user=${user}&password=${password}&dbName=${dbName}`;
        this.http.get(`${url}tables?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyTables(value.json());
        });
    }

    public getColumns(url: string, ip: string, port: number, user: string, password: string, dbName: string, tblName: string) {
        let query: string =
            `host=${ip}&port=${port}&user=${user}&password=${password}&dbName=${dbName}&tableName=${tblName}`;
        this.http.get(`${url}columns?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyColumns(value.json());
        });
    }
}