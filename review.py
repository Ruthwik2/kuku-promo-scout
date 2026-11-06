"""Validate and apply a free-tool AI/editor review, bound to exact source hashes."""
import argparse,json
from pathlib import Path
from scout import load_pack,candidates,validate_review,save_report,stamp,VERSION

def apply_review(input_path,review_path,out):
    eps,errors=load_pack(input_path)
    if errors:raise ValueError(errors)
    review=json.loads(Path(review_path).read_text());records=review['episodes'];ids=[r['episode'] for r in records]
    if len(ids)!=len(set(ids)) or set(ids)!={e['episode'] for e in eps}:raise ValueError('Review must cover each input episode exactly once')
    selected=[]
    for ep in eps:
        if review['source_hashes'].get(str(ep['episode']))!=ep['sha256']:raise ValueError('Review is stale: input hash mismatch')
        row=next(r for r in records if r['episode']==ep['episode']);pool=candidates(ep);validate_review(row,pool);index={c['id']:c for c in pool}
        for s in row['selections']:
            c=index[s['candidate_id']];c['model_review']=s;c['score']=7*s['hook']+7*s['cliffhanger']+6*s['standalone'];c['score_type']='assisted_review_rubric_not_probability';c['why']=s['why'];c['heuristic_flags']=c['flags'];c['flags']=[s['risk']];c['review_status']='AI_reviewed_editor_approval_pending'
            for field in ('hook','cliffhanger'):
                eid=s.get(field+'_event_id')
                if eid:
                    event=next((e for e in ep['events'] if e['id']==eid),None);seg=c['segments'][0]
                    if not event or not seg['start_seconds']<=event['start']<seg['end_seconds']:raise ValueError('Review evidence outside clip')
                    c[field]=dict(event_id=eid,timestamp=stamp(event['start']),text=event['text'])
            selected.append(c)
    selected.sort(key=lambda c:(-c['score'],c['id']))
    report=dict(tool='Promo Scout',version=VERSION,mode='assisted_review',review_method=review['method'],parsed_episodes=len(eps),input_episodes=len(eps),full_pack_complete=True,selected_count=len(selected),candidate_count=sum(r['candidate_count'] for r in review['coverage']),promos=selected,posting_queue_ids=[c['id'] for c in selected[:10]],coverage=review['coverage'],errors=[],model_errors=[],limitations=['AI editorial review is not independent human validation.','Reviews are bound to exact source hashes; new input needs a fresh review or API run.','Continuous source clips only. Verify performance, timing and suitability against video.'],audit=records)
    save_report(report,out);return report
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('review');p.add_argument('--out',default='runs/reviewed');a=p.parse_args();r=apply_review(a.input,a.review,a.out);print(f"Validated {len(r['audit'])} episode reviews; {len(r['promos'])} shortlisted clips")
