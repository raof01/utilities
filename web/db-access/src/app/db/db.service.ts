import { Injectable, EventEmitter } from '@angular/core';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { HubService } from '../hub.service';
@Injectable()
export class DbService {

    constructor(private http: Http, private hubService: HubService) {
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
            this.hubService.notifyDbs(value.json());
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
            this.hubService.notifyTables(value.json());
        });
    }
}