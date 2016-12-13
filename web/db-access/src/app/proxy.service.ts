import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class Proxy {
    private dbsSubject: Subject<string[]>;
    private tablesSubject: Subject<string[]>;
    private dbSelectedSubject: Subject<string>;
    private tblSelectedSubject: Subject<string>;
    private fieldsSubject: Subject<string[]>;
    private rowsSubject: Subject<any[]>;

    constructor() {
        this.dbsSubject = new Subject();
        this.tablesSubject = new Subject();
        this.dbSelectedSubject = new Subject();
        this.tblSelectedSubject = new Subject();
        this.fieldsSubject = new Subject();
        this.rowsSubject = new Subject();
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

    public notifyTableSelected(v: string) {
        this.tblSelectedSubject.next(v);
    }

    public subscribeTableSelected(fn) {
        this.tblSelectedSubject.subscribe(fn);
    }

    public subscribeFields(fn) {
        this.fieldsSubject.subscribe(fn);
    }

    public notifyFields(v: string[]) {
        this.fieldsSubject.next(v);
    }

    public subscribeRows(fn) {
        this.rowsSubject.subscribe(fn);
    }

    public notifyRows(v: any[]) {
        this.rowsSubject.next(v);
    }
}