import {AfterViewInit, ChangeDetectorRef, Component, OnInit, ViewChild} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {FormControl, Validators} from '@angular/forms';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewInit {

  @ViewChild('repliesList') repliesList;
  @ViewChild('repliesDiv') repliesDiv;

  apis: string[] = [];
  history: string[] = [];
  query: string;

  result: any;

  replies: any[] = [];
  private selectedApi: string;

  recognition;
  speechRecognitionList;
  private baseApiUrl: string = 'http://localhost:8000';

  constructor(private http: HttpClient,
              private _cdr: ChangeDetectorRef,
              private _snackBar: MatSnackBar) {
  }

  ngAfterViewInit(): void {

    this.http.get(this.baseApiUrl + '/api/', {headers: new HttpHeaders({
        Authorization: localStorage.getItem('access_token')
      })}).subscribe(apis => (apis as any[]).forEach(api => this.apis.push(api)));
    this.http.get(this.baseApiUrl + '/history/', {headers: new HttpHeaders({
        Authorization: localStorage.getItem('access_token')
      })}).subscribe(histories => {
      this.history = histories["history"] as string[];
    });

    setTimeout(() => {
      this.scrollToLastReply();
    }, 100);
  }

  ngOnInit(): void {
    // this.populateChatHistory();
    this.initSpeechRecognition();
  }

  sendQuery(query: string) {

    if (!this.selectedApi) {
      this._snackBar.open('Please select an API', '', {
        duration: 2000,
      });

      return;
    }

    this.replies = [...this.replies, {
      content: query,
      author: 'user'
    }];

    let params = new HttpParams().set('sentence', query);

    this.http.get('http://localhost:8000/query/' + this.selectedApi, {params: params, headers: new HttpHeaders({
        Authorization: localStorage.getItem('access_token')
      })}).subscribe(result => {
      this.result = result;
    });

    setTimeout(() => {
      this.scrollToLastReply();
    }, 1);

  }

  apiSelected(api: string) {
    this.selectedApi = api;

    this.replies = [];
    this.history.forEach((reply: any) =>
    {
      if (reply.api === this.selectedApi) {
        this.replies.push({
          content: reply.sentence,
          author: 'user',
          response: reply.result
        })
      }
    })
  }

  getReplyUserImage(reply: any) {
    if (reply.author === 'AI') {
      return '../../assets/desktop_mac-24px.svg';
    }

    if (reply.author === 'user') {
      return '../../assets/account_circle-24px.svg';
    }
  }

  private scrollToLastReply() {
    if (this.repliesDiv.nativeElement.children[this.repliesDiv.nativeElement.children.length - 1]) {
      this.repliesDiv.nativeElement.children[this.repliesDiv.nativeElement.children.length - 1].scrollIntoView();
    }
  }

  startListening() {
    this.recognition.start();
  }


  private initSpeechRecognition() {
    var SpeechRecognition = SpeechRecognition || window['webkitSpeechRecognition'];
    var SpeechGrammarList = SpeechGrammarList || window['webkitSpeechGrammarList'];

    this.recognition = new SpeechRecognition();
    this.speechRecognitionList = new SpeechGrammarList();
    this.recognition.grammars = this.speechRecognitionList;
    this.recognition.continuous = true;
    this.recognition.lang = 'en-US';
    this.recognition.interimResults = true;
    this.recognition.maxAlternatives = 1;

    let that = this;
    this.recognition.onresult = function(event) {
      for (var i = event.resultIndex; i < event.results.length; i++) {
        that.query = event.results[i][0].transcript;
        that._cdr.detectChanges();
      }
    };

    this.recognition.onspeechend = function() {
      that.recognition.stop();
    };

    this.recognition.onnomatch = function(event) {
      console.log('did not recognize', event);
    };

    this.recognition.onerror = function(event) {
      console.log('error', event);
    };
  }

  onChange(event: any) {
    var file = event.target.files[0];

    if (!file) {
      return;
    }

    const formData = new FormData();

    formData.append("file", file, file.name);

    this.http.post(this.baseApiUrl + '/upload/', formData, {headers: new HttpHeaders({
        Authorization: localStorage.getItem('access_token')
      })}).subscribe(response =>
    this.apis.push(file.name.split('.')[0]));
  }

  getResponseForReply(clickedReply: any) {
    this.replies.forEach(reply => {
      if (clickedReply.content === reply.content) {
        this.result = reply.response;
      }
    });

  }
}
