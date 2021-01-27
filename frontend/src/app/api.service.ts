import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, of} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseApiUrl: string = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  sendGetRequest(url: string) : any {
    this.http.get(url).subscribe(data => { return of(data); },
      error => {
      this.http.post(this.baseApiUrl + '/refresh', {
        refresh_token: localStorage.getItem('refresh_token')
      }).subscribe(response => {
        localStorage.setItem('access_token', response['access_token']);
        localStorage.setItem('refresh_token', response['refresh_token']);
      });

      return this.http.get(url);
    });
  }

  sendPostRequest(url: string, body: any) : any {
    this.http.post(url, body).subscribe(data => { return of(data); },
      error => {
        this.http.post(this.baseApiUrl + '/refresh', {
          refresh_token: localStorage.getItem('refresh_token')
        }).subscribe(response => {
          localStorage.setItem('access_token', response['access_token']);
          localStorage.setItem('refresh_token', response['refresh_token']);
        });

        return this.http.post(url, body);
      });
  }

}
