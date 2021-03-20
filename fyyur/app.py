# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    jsonify
)
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from model import Artist, Venue, Show, Genres, db, init

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
with app.app_context():
    db.init_app(app)
    init()
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []
    currentDateTime = datetime.today()
    for [city, state] in Venue.query.with_entities(Venue.city, Venue.state).distinct():
        venues = []
        for venue in Venue.query.filter_by(city=city).all():
            venueInfo = {
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': Show.query.filter(Show.venue_id == venue.id,
                                                        Show.start_time >= currentDateTime).count()
            }
            venues.append(venueInfo)
        cityInfo = {
            'city': city,
            'state': state,
            'venues': venues
        }
        data.append(cityInfo)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    venues = []
    currentDateTime = datetime.today()
    venueName = request.form.get('search_term')
    for venue in Venue.query.filter(Venue.name.ilike("%{}%".format(venueName))).all():
        venueInfo = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': Show.query.filter(Show.venue_id == venue.id,
                                                    Show.start_time >= currentDateTime).count()
        }
        venues.append(venueInfo)

    response = {
        'count': len(venues),
        'data': venues
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    currentDateTime = datetime.today()
    venue = Venue.query.filter_by(id=venue_id).first()
    pastShows = []
    upcomingShows = []
    for show in venue.shows:
        showInfo = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.isoformat() + ".000Z"
        }
        if show.start_time >= currentDateTime:
            upcomingShows.append(showInfo)
        else:
            pastShows.append(showInfo)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": [g.name for g in venue.genres],
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": pastShows,
        "upcoming_shows": upcomingShows,
        "past_shows_count": len(pastShows),
        "upcoming_shows_count": len(upcomingShows),
    }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        venueData = request.form
        venueName = venueData.get('name')
        venueCity = venueData.get('city')
        venueState = venueData.get('state')
        venueAddress = venueData.get('address')
        venuePhone = venueData.get('phone')
        venueFacebookLink = venueData.get('facebook_link')
        venueGenresList = venueData.getlist('genres')
        venue = Venue(name=venueName,
                      city=venueCity,
                      state=venueState,
                      address=venueAddress,
                      phone=venuePhone,
                      facebook_link=venueFacebookLink
                      )
        for venueGenres in venueGenresList:
            if Genres.query.filter_by(name=venueGenres).first():
                venue.genres.append(Genres.query.filter_by(name=venueGenres).first())
            else:
                genres = Genres(name=venueGenres)
                venue.genres.append(genres)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed!')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        venue.genres = []
        db.session.delete(venue)
        db.session.commit()
        response = {'success': True,
                    'id': venue_id
                    }
        flash('Venue ' + venue.name + ' was successfully deleted!')
    except:
        db.session.rollback()
        response = {'success': False,
                    'id': venue_id
                    }
        flash('An error occurred. Venue ' + venue.name + ' could not be deleted!')
    finally:
        db.session.close()
    return jsonify(response)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = []
    for artist in Artist.query.all():
        artistInfo = {
            'id': artist.id,
            'name': artist.name
        }
        data.append(artistInfo)

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    artists = []
    currentDateTime = datetime.today()
    artistName = request.form.get('search_term')
    for artist in Artist.query.filter(Artist.name.ilike("%{}%".format(artistName))).all():
        artistInfo = {
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': Show.query.filter(Show.artist_id == artist.id,
                                                    Show.start_time >= currentDateTime).count()
        }
        artists.append(artistInfo)

    response = {
        'count': len(artists),
        'data': artists
    }

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    currentDateTime = datetime.today()
    artist = Artist.query.filter_by(id=artist_id).first()
    pastShows = []
    upcomingShows = []
    for show in artist.shows:
        showInfo = {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.isoformat() + ".000Z"
        }
        if show.start_time >= currentDateTime:
            upcomingShows.append(showInfo)
        else:
            pastShows.append(showInfo)

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": [g.name for g in artist.genres],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": pastShows,
        "upcoming_shows": upcomingShows,
        "past_shows_count": len(pastShows),
        "upcoming_shows_count": len(upcomingShows)
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()
    artistInfo = {
        "id": artist.id,
        "name": artist.name,
        "genres": [e.name for e in artist.genres],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link
    }
    return render_template('forms/edit_artist.html', form=form, artist=artistInfo)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    newArtistData = request.form
    oldArtistData = Artist.query.filter_by(id=artist_id).first()
    oldArtistData.name = newArtistData.get('name')
    oldArtistData.phone = newArtistData.get('phone')
    oldArtistData.city = newArtistData.get('city')
    oldArtistData.state = newArtistData.get('state')
    oldArtistData.facebook_link = newArtistData.get('facebook_link')
    oldArtistData.genres = []
    for artistGenres in newArtistData.getlist('genres'):
        if Genres.query.filter_by(name=artistGenres).first():
            oldArtistData.genres.append(Genres.query.filter_by(name=artistGenres).first())
        else:
            genres = Genres(name=artistGenres)
            oldArtistData.genres.append(genres)
    db.session.commit()
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()
    venueInfo = {
        "id": venue.id,
        "name": venue.name,
        "genres": [e.name for e in venue.genres],
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link
    }

    return render_template('forms/edit_venue.html', form=form, venue=venueInfo)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    newVenueData = request.form
    oldVenueData = Venue.query.filter_by(id=venue_id).first()
    oldVenueData.name = newVenueData.get('name')
    oldVenueData.phone = newVenueData.get('phone')
    oldVenueData.city = newVenueData.get('city')
    oldVenueData.state = newVenueData.get('state')
    oldVenueData.facebook_link = newVenueData.get('facebook_link')
    oldVenueData.genres = []
    for venueGenres in newVenueData.getlist('genres'):
        if Genres.query.filter_by(name=venueGenres).first():
            oldVenueData.genres.append(Genres.query.filter_by(name=venueGenres).first())
        else:
            genres = Genres(name=venueGenres)
            oldVenueData.genres.append(genres)
    db.session.commit()
    db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        artistData = request.form
        artistName = artistData.get('name')
        artistPhone = artistData.get('phone')
        artistCity = artistData.get('city')
        artistState = artistData.get('state')
        artistFacebookLink = artistData.get('facebook_link')
        artistGenresList = artistData.getlist('genres')
        artist = Artist(name=artistName,
                        phone=artistPhone,
                        city=artistCity,
                        state=artistState,
                        facebook_link=artistFacebookLink
                        )
        for artistGenres in artistGenresList:
            if Genres.query.filter_by(name=artistGenres).first():
                artist.genres.append(Genres.query.filter_by(name=artistGenres).first())
            else:
                genres = Genres(name=artistGenres)
                artist.genres.append(genres)
        db.session.add(artist)
        db.session.commit()
        flash('artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. artist ' + request.form['name'] + ' could not be listed!')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    for show in Show.query.all():
        showInfo = {'venue_id': show.venue_id,
                    'venue_name': show.venue.name,
                    'artist_id': show.artist_id,
                    'artist_name': show.artist.name,
                    'artist_image_link': show.artist.image_link,
                    'start_time': show.start_time.isoformat() + ".000Z"
                    }
        data.append(showInfo)
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        showData = request.form
        showVenueId = showData.get('venue_id')
        showArtistId = showData.get('artist_id')
        showStartTime = showData.get('start_time')
        if not Venue.query.filter_by(id=showVenueId).first():
            flash('The venue does not exist. Please find the venue id from the venues page.')
        elif not Artist.query.filter_by(id=showArtistId).first():
            flash('The artist does not exist. Please find the artist id from the venues page.')
        else:
            show = Show(venue_id=showVenueId,
                        artist_id=showArtistId,
                        start_time=showStartTime
                        )
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('Show could not be listed!')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
