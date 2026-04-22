#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
if not data:
    print("No active sessions")
    sys.exit(0)

session = data[0]
ps = session.get('PlayState', {})
now_playing = session.get('NowPlayingItem', None)

print("Currently Playing:")
print("=" * 60)
if now_playing:
    print(f"Song: {now_playing.get('Name', 'Unknown')}")
    artists = now_playing.get('Artists', ['Unknown'])
    print(f"Artist: {', '.join(artists)}")
    print(f"Album: {now_playing.get('Album', 'Unknown')}")
    duration = now_playing.get('RunTimeTicks', 0) / 10000000
    print(f"Duration: {duration:.1f}s")
    position = ps.get('PositionTicks', 0) / 10000000
    if duration > 0:
        percent = (position / duration) * 100
    else:
        percent = 0
    print(f"Position: {position:.1f}s ({percent:.1f}%)")
    print(f"Paused: {ps.get('IsPaused', False)}")
    print(f"Muted: {ps.get('IsMuted', False)}")
else:
    print("Nothing is playing right now")
