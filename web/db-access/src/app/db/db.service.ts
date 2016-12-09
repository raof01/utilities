import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';

@Injectable()
export class DbService {
    private dbsSubject: Subject<string[]>;
    constructor(private http: Http) {
        this.dbsSubject = new Subject();
    }

    public subscribeDbs(fn) {
        this.dbsSubject.subscribe(fn);
    }
    
    public getDbs(ip: string, port: number, user: string, password: string) : void {
        let url: string = 'http://localhost:3000/dbs';
        /*let body: string = `{
            host: ${ip},
            port: ${port},
            user: ${user},
            password: ${password}
        }`;*/
        let query: string =
            `host=${ip}&port=${port}&user=${user}&password=${password}`;
        this.http.get(`${url}?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            console.log(value.json());
        });
    }
}