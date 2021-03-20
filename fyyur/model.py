from flask_sqlalchemy import SQLAlchemy
from data import artists, venues

db = SQLAlchemy()
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
venue_genres = db.Table('venue_genres',
                        db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
                        db.Column('genres_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
                        )

artist_generes = db.Table('artist_genres',
                          db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
                          db.Column('genres_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
                          )


class Show(db.Model):
    __tablename__ = 'show'

    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, primary_key=True)
    venue = db.relationship("Venue", back_populates='shows')
    artist = db.relationship('Artist', back_populates='shows')


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(255))
    seeking_talent = db.Column(db.Boolean, server_default='false', default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.relationship('Genres', secondary=venue_genres, backref=db.backref('venues', lazy=True))
    shows = db.relationship('Show', back_populates='venue')


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(255))
    seeking_venue = db.Column(db.Boolean, server_default='false', default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.relationship('Genres', secondary=artist_generes, backref=db.backref('artists', lazy=True))
    shows = db.relationship('Show', back_populates='artist')


class Genres(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))


# ----------------------------------------------------------------------------#
# Populate original dataset
# ----------------------------------------------------------------------------#
def init():
    if Artist.query.count() == 0:
        for artist in artists:
            artistId = artist.get('id')
            artistName = artist.get('name')
            artistCity = artist.get('city')
            artistState = artist.get('state')
            artistPhone = artist.get('phone')
            artistSeekingVenue = artist.get('seeking_venue')
            artistSeekingDescription = artist.get('seeking_description')
            artistWebsite = artist.get('website')
            artistImageLink = artist.get('image_link')
            artistFacebookLink = artist.get('facebook_link')
            artistData = Artist(name=artistName,
                                city=artistCity,
                                state=artistState,
                                phone=artistPhone,
                                seeking_venue=artistSeekingVenue,
                                seeking_description=artistSeekingDescription,
                                website=artistWebsite,
                                image_link=artistImageLink,
                                facebook_link=artistFacebookLink
                                )
            for artistGenres in artist.get('genres'):
                if Genres.query.filter_by(name=artistGenres).first():
                    artistData.genres.append(Genres.query.filter_by(name=artistGenres).first())
                else:
                    genres = Genres(name=artistGenres)
                    artistData.genres.append(genres)
            db.session.add(artistData)
            db.session.commit()

        db.session.close()

    if Venue.query.count() == 0:
        for venue in venues:
            venueId = venue.get('id')
            venueName = venue.get('name')
            venueCity = venue.get('city')
            venueState = venue.get('state')
            venueAddress = venue.get('address')
            venuePhone = venue.get('phone')
            venueSeekingTalent = venue.get('seeking_talent')
            venueSeekingDescription = venue.get('seeking_description')
            venueWebsite = venue.get('website')
            venueImageLink = venue.get('image_link')
            venueFacebookLink = venue.get('facebook_link')
            venueData = Venue(name=venueName,
                              city=venueCity,
                              state=venueState,
                              address=venueAddress,
                              phone=venuePhone,
                              seeking_talent=venueSeekingTalent,
                              seeking_description=venueSeekingDescription,
                              website=venueWebsite,
                              image_link=venueImageLink,
                              facebook_link=venueFacebookLink
                              )

            for venueGenres in venue.get('genres'):
                if Genres.query.filter_by(name=venueGenres).first():
                    venueData.genres.append(Genres.query.filter_by(name=venueGenres).first())
                else:
                    genres = Genres(name=venueGenres)
                    venueData.genres.append(genres)
            db.session.add(venueData)
            db.session.commit()

        db.session.close()

    if Show.query.count() == 0:
        for artist in artists:
            artistName = artist.get('name')
            artistData = Artist.query.filter_by(name=artistName).first()
            for pastShow in artist.get('past_shows'):
                venueName = pastShow.get('venue_name')
                venueData = Venue.query.filter_by(name=venueName).first()
                startTime = pastShow.get('start_time')
                if Show.query.filter_by(venue_id=venueData.id, artist_id=artistData.id,
                                        start_time=startTime).count() == 0:
                    show = Show(start_time=startTime, venue=venueData, artist=artistData)
                    db.session.add(show)
                    db.session.commit()

            for upcomingShow in artist.get('upcoming_shows'):
                venueName = upcomingShow.get('venue_name')
                venueData = Venue.query.filter_by(name=venueName).first()
                startTime = upcomingShow.get('start_time')
                if Show.query.filter_by(venue_id=venueData.id, artist_id=artistData.id,
                                        start_time=startTime).count() == 0:
                    show = Show(start_time=startTime, venue=venueData, artist=artistData)
                    db.session.add(show)
                    db.session.commit()

        for venue in venues:
            venueName = venue.get('name')
            venueData = Venue.query.filter_by(name=venueName).first()
            for pastShow in venue.get('past_shows'):
                artistName = pastShow.get('artist_name')
                artistData = Artist.query.filter_by(name=artistName).first()
                startTime = pastShow.get('start_time')
                if Show.query.filter_by(venue_id=venueData.id, artist_id=artistData.id,
                                        start_time=startTime).count() == 0:
                    show = Show(start_time=startTime, venue=venueData, artist=artistData)
                    db.session.add(show)
                    db.session.commit()

            for upcomingShow in venue.get('upcoming_shows'):
                artistName = upcomingShow.get('artist_name')
                artistData = Artist.query.filter_by(name=artistName).first()
                startTime = upcomingShow.get('start_time')
                if Show.query.filter_by(venue_id=venueData.id, artist_id=artistData.id,
                                        start_time=startTime).count() == 0:
                    show = Show(start_time=startTime, venue=venueData, artist=artistData)
                    db.session.add(show)
                    db.session.commit()
        db.session.close()
