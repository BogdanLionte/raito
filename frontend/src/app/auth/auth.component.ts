import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {
  private baseApiUrl: string = 'http://localhost:8000';

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
  }

  login(){
    this.http.get(this.baseApiUrl + '/auth/').subscribe(AuthObj => {window.open(AuthObj['auth']); });
    window.addEventListener('message', (event) => {
      console.log('origin=' + event.origin);
      if (event.origin !== this.baseApiUrl){
        return;
      }
      const result = JSON.parse(event.data);
      localStorage.setItem('access_token', result['access_token']);
      localStorage.setItem('refresh_token', result['refresh_token']);
      this.router.navigateByUrl('/chat');
    }, false);
  }
}
