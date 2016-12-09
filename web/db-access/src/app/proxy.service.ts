import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class Proxy {
    private dbsSubject: Subject<string[]>;
    private tablesSubject: Subject<string[]>;
    private dbSelectedSubject: Subject<string>;

    constructor() {
        this.dbsSubject = new Subject();
        this.tablesSubject = new Subject();
        this.dbSelectedSubject = new Subject();
    }

    public subscribeDbs(fn) {
        this.dbsSubject.subscribe(fn);
    }

    public subscribeTables(fn) {
        this.tablesSubject.subscribe(fn);
    }

    public subscribeDbSelected(fn) {
        this.dbSelectedSubject.subscribe(fn);
    }

    public notifyDbSelected(v: string) {
        this.dbSelectedSubject.next(v);
    }

    public notifyDbs(v: string[]) {
        this.dbsSubject.next(v);
    }

    public notifyTables(v: string[]) {
        this.tablesSubject.next(v);
    }
}