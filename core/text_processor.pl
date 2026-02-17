#!/usr/bin/perl
use strict;
use warnings;
use JSON;
use POSIX qw(strftime);

# Tanya - Text Processing Engine (Perl)
# High-speed text normalization and processing

package TextProcessor;

sub new {
    my ($class, %args) = @_;
    return bless {
        stopwords => _load_stopwords(),
        min_word_len => $args{min_word_len} // 3,
    }, $class;
}

sub _load_stopwords {
    return {
        map { $_ => 1 } qw(
            the a an and or but in on at to for of with by from
            is are was were be been being have has had do does did
            will would could should may might must shall this that
            these those i you he she it we they what which who when
            where why how
        )
    };
}

sub normalize_text {
    my ($self, $text) = @_;
    
    # Lowercase
    $text = lc($text);
    
    # Remove HTML tags
    $text =~ s/<[^>]+>//g;
    
    # Remove URLs
    $text =~ s/http\S+//g;
    
    # Remove special characters, keep alphanumeric and spaces
    $text =~ s/[^\w\s]//g;
    
    # Remove extra whitespace
    $text =~ s/\s+/ /g;
    $text =~ s/^\s+|\s+$//g;
    
    return $text;
}

sub tokenize {
    my ($self, $text) = @_;
    
    $text = $self->normalize_text($text);
    
    my @words = split /\s+/, $text;
    
    # Filter by length and stopwords
    @words = grep {
        length($_) >= $self->{min_word_len} 
        && !exists $self->{stopwords}{$_}
    } @words;
    
    return \@words;
}

sub calculate_reading_time {
    my ($self, $text) = @_;
    
    my $words = $self->tokenize($text);
    my $word_count = scalar @$words;
    my $wpm = 200; # Average reading speed
    
    return POSIX::ceil($word_count / $wpm);
}

sub extract_keywords {
    my ($self, $text, $top_n) = @_;
    
    $top_n //= 10;
    
    my $tokens = $self->tokenize($text);
    my %freq;
    
    $freq{$_}++ for @$tokens;
    
    my @sorted = sort { $freq{$b} <=> $freq{$a} } keys %freq;
    
    return [
        map { 
            { 
                keyword => $_, 
                count => $freq{$_},
                score => sprintf("%.2f", $freq{$_} / scalar(@$tokens) * 100)
            } 
        } splice(@sorted, 0, $top_n)
    ];
}

sub calculate_similarity {
    my ($self, $text1, $text2) = @_;
    
    my $tokens1 = $self->tokenize($text1);
    my $tokens2 = $self->tokenize($text2);
    
    my %set1 = map { $_ => 1 } @$tokens1;
    my %set2 = map { $_ => 1 } @$tokens2;
    
    my @intersection = grep { $set1{$_} && $set2{$_} } keys %set1;
    my @union = (keys %set1, keys %set2);
    my %seen;
    @union = grep { !$seen{$_}++ } @union;
    
    return 0 if scalar(@union) == 0;
    
    return scalar(@intersection) / scalar(@union);
}

1;

package main;

# Demo
my $processor = TextProcessor->new(min_word_len => 4);

my $sample = "This is a sample article about artificial intelligence and machine learning. 
AI is a breakthrough technology that helps computers learn from data. Machine learning 
is a subset of AI that enables predictive analytics.";

print "=== Text Normalization ===\n";
print $processor->normalize_text($sample) . "\n\n";

print "=== Keywords ===\n";
my $keywords = $processor->extract_keywords($sample, 5);
print JSON->new->pretty->encode($keywords);

print "\n=== Reading Time ===\n";
print $processor->calculate_reading_time($sample) . " minutes\n";
